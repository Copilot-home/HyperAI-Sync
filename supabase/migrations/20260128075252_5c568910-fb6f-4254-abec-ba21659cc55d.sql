-- ============================================
-- ECVM DATABASE SCHEMA & ENFORCEMENT LAYER
-- Spec: ECVM-CS-1.0 (FULL · UNIFIED · LOCKED)
-- Kernel: MONOLITHIC KERNEL v0.1.3
-- ============================================

-- ===========================================
-- 1. ROLE MANAGEMENT (for admin vs user)
-- ===========================================

create type public.app_role as enum ('admin', 'user');

create table public.user_roles (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete cascade not null,
    role app_role not null default 'user',
    created_at timestamptz not null default now(),
    unique (user_id, role)
);

alter table public.user_roles enable row level security;

-- Security definer function to check roles (avoids RLS recursion)
create or replace function public.has_role(_user_id uuid, _role app_role)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.user_roles
    where user_id = _user_id
      and role = _role
  )
$$;

-- RLS for user_roles
create policy "Users can view own roles"
on public.user_roles for select
using (user_id = auth.uid());

create policy "Service role manages roles"
on public.user_roles for all
using (auth.role() = 'service_role');

-- ===========================================
-- 2. CORE ENUMS (LOCKED)
-- ===========================================

create type public.identity_state_enum as enum (
    'NO_IDENTITY',
    'INSUFFICIENT',
    'ESTABLISHED',
    'DRIFT'
);

create type public.task_type_enum as enum (
    'image_static',
    'image',
    'video',
    'validation'
);

create type public.kernel_verdict_enum as enum (
    'PASS',
    'REJECT',
    'HALT'
);

create type public.drift_type_enum as enum (
    'PER_NODE',
    'SYSTEMIC'
);

-- ===========================================
-- 3. ENTITY IDENTITY (IMMUTABLE CORE)
-- ===========================================

create table public.entity_identity (
    entity_id uuid primary key default gen_random_uuid(),
    owner_user_id uuid not null references auth.users(id) on delete cascade,
    identity_hash char(64) not null,
    geometry_hash char(64) not null,
    created_at timestamptz not null default now(),
    locked boolean not null default true
);

-- IMMUTABILITY TRIGGER: Block UPDATE/DELETE
create or replace function public.forbid_identity_update()
returns trigger as $$
begin
    raise exception 'IDENTITY_IMMUTABLE: Cannot modify or delete identity records';
end;
$$ language plpgsql;

create trigger trg_identity_no_update
before update or delete on public.entity_identity
for each row execute function public.forbid_identity_update();

-- RLS: Owner can only READ
alter table public.entity_identity enable row level security;

create policy "entity_owner_read"
on public.entity_identity for select
using (owner_user_id = auth.uid());

create policy "entity_owner_insert"
on public.entity_identity for insert
with check (owner_user_id = auth.uid());

create policy "service_role_all"
on public.entity_identity for all
using (auth.role() = 'service_role');

-- ===========================================
-- 4. IDENTITY STATE (SYSTEM-OWNED)
-- ===========================================

create table public.identity_state (
    entity_id uuid primary key references public.entity_identity(entity_id) on delete cascade,
    state identity_state_enum not null default 'NO_IDENTITY',
    variance_score float not null default 1.0,
    coverage_percent float not null default 0.0,
    updated_at timestamptz not null default now()
);

-- RLS: User READ only, System UPDATE
alter table public.identity_state enable row level security;

create policy "identity_state_user_read"
on public.identity_state for select
using (
    entity_id in (
        select entity_id from public.entity_identity
        where owner_user_id = auth.uid()
    )
);

create policy "identity_state_service_all"
on public.identity_state for all
using (auth.role() = 'service_role');

-- Auto-create identity_state when entity_identity is inserted
create or replace function public.create_identity_state()
returns trigger as $$
begin
    insert into public.identity_state (entity_id, state, variance_score)
    values (new.entity_id, 'NO_IDENTITY', 1.0);
    return new;
end;
$$ language plpgsql security definer;

create trigger trg_create_identity_state
after insert on public.entity_identity
for each row execute function public.create_identity_state();

-- ===========================================
-- 5. LOGIC MODULE (ADMIN-OWNED · SYSTEM BRAIN)
-- ===========================================

create table public.logic_module (
    logic_id uuid primary key default gen_random_uuid(),
    name text not null,
    description text,
    task_type task_type_enum not null,
    required_identity_state identity_state_enum not null default 'ESTABLISHED',
    camera_profile jsonb not null default '{}',
    motion_profile jsonb not null default '{}',
    drift_risk_score float not null default 0.5,
    enabled boolean not null default false,
    version int not null default 1,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- RLS: Admin only (via service_role or has_role)
alter table public.logic_module enable row level security;

create policy "logic_module_read"
on public.logic_module for select
using (true);

create policy "logic_module_admin_write"
on public.logic_module for all
using (
    auth.role() = 'service_role' 
    or public.has_role(auth.uid(), 'admin')
);

-- ===========================================
-- 6. LOGIC VERSION HISTORY (AUDIT)
-- ===========================================

create table public.logic_version_history (
    logic_id uuid references public.logic_module(logic_id) on delete cascade,
    version int not null,
    snapshot jsonb not null,
    changed_at timestamptz not null default now(),
    changed_by uuid,
    primary key (logic_id, version)
);

alter table public.logic_version_history enable row level security;

create policy "logic_history_read"
on public.logic_version_history for select
using (public.has_role(auth.uid(), 'admin') or auth.role() = 'service_role');

-- Trigger to save snapshot on logic_module update
create or replace function public.save_logic_version()
returns trigger as $$
begin
    insert into public.logic_version_history (logic_id, version, snapshot, changed_by)
    values (
        old.logic_id,
        old.version,
        to_jsonb(old),
        auth.uid()
    );
    new.version := old.version + 1;
    new.updated_at := now();
    return new;
end;
$$ language plpgsql security definer;

create trigger trg_logic_version_history
before update on public.logic_module
for each row execute function public.save_logic_version();

-- ===========================================
-- 7. TASK EXECUTION LOG
-- ===========================================

create table public.task_execution_log (
    task_id uuid primary key default gen_random_uuid(),
    entity_id uuid references public.entity_identity(entity_id) on delete cascade not null,
    logic_id uuid references public.logic_module(logic_id) on delete set null,
    task_type task_type_enum not null,
    verdict kernel_verdict_enum not null,
    logic_applied text[] not null default '{}',
    execution_time_ms int not null default 0,
    metadata jsonb not null default '{}',
    executed_at timestamptz not null default now()
);

alter table public.task_execution_log enable row level security;

-- User can read own entity's logs
create policy "task_log_user_read"
on public.task_execution_log for select
using (
    entity_id in (
        select entity_id from public.entity_identity
        where owner_user_id = auth.uid()
    )
);

-- Service role (Kernel) writes
create policy "task_log_service_write"
on public.task_execution_log for all
using (auth.role() = 'service_role');

-- Admin can read all
create policy "task_log_admin_read"
on public.task_execution_log for select
using (public.has_role(auth.uid(), 'admin'));

-- ===========================================
-- 8. DRIFT EVENT
-- ===========================================

create table public.drift_event (
    drift_id uuid primary key default gen_random_uuid(),
    entity_id uuid references public.entity_identity(entity_id) on delete cascade,
    logic_id uuid references public.logic_module(logic_id) on delete set null,
    drift_type drift_type_enum not null,
    severity float not null,
    baseline float not null default 0.0,
    current_value float not null default 0.0,
    acknowledged boolean not null default false,
    detected_at timestamptz not null default now()
);

-- Trigger to auto-classify drift type
create or replace function public.classify_drift()
returns trigger as $$
begin
    if new.logic_id is not null then
        new.drift_type := 'SYSTEMIC';
    else
        new.drift_type := 'PER_NODE';
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trg_classify_drift
before insert or update on public.drift_event
for each row execute function public.classify_drift();

alter table public.drift_event enable row level security;

-- User reads own drift
create policy "drift_user_read"
on public.drift_event for select
using (
    entity_id in (
        select entity_id from public.entity_identity
        where owner_user_id = auth.uid()
    )
);

-- Admin reads all, service writes
create policy "drift_admin_read"
on public.drift_event for select
using (public.has_role(auth.uid(), 'admin'));

create policy "drift_service_all"
on public.drift_event for all
using (auth.role() = 'service_role');

-- ===========================================
-- 9. UNMET LOGIC SIGNAL (USER → ADMIN)
-- ===========================================

create table public.unmet_logic_signal (
    signal_id uuid primary key default gen_random_uuid(),
    entity_id uuid references public.entity_identity(entity_id) on delete cascade not null,
    requested_task task_type_enum not null,
    observed_state identity_state_enum not null,
    reason text,
    severity text not null default 'medium',
    created_at timestamptz not null default now()
);

alter table public.unmet_logic_signal enable row level security;

-- User can insert for own entity
create policy "unmet_user_insert"
on public.unmet_logic_signal for insert
with check (
    entity_id in (
        select entity_id from public.entity_identity
        where owner_user_id = auth.uid()
    )
);

-- Admin reads all
create policy "unmet_admin_read"
on public.unmet_logic_signal for select
using (public.has_role(auth.uid(), 'admin') or auth.role() = 'service_role');

-- Admin can delete after synthesis
create policy "unmet_admin_delete"
on public.unmet_logic_signal for delete
using (public.has_role(auth.uid(), 'admin') or auth.role() = 'service_role');

-- ===========================================
-- 10. AUDIT LOG (SYSTEM-WIDE)
-- ===========================================

create table public.audit_log (
    id uuid primary key default gen_random_uuid(),
    action text not null,
    actor_type text not null check (actor_type in ('user', 'system', 'service_role')),
    actor_id text not null,
    resource_type text not null,
    resource_id text not null,
    details jsonb not null default '{}',
    timestamp timestamptz not null default now()
);

alter table public.audit_log enable row level security;

-- Only admin/service can read
create policy "audit_admin_read"
on public.audit_log for select
using (public.has_role(auth.uid(), 'admin') or auth.role() = 'service_role');

-- Only service role can insert
create policy "audit_service_insert"
on public.audit_log for insert
with check (auth.role() = 'service_role');

-- ===========================================
-- 11. INDEXES FOR PERFORMANCE
-- ===========================================

create index idx_entity_identity_owner on public.entity_identity(owner_user_id);
create index idx_identity_state_state on public.identity_state(state);
create index idx_task_log_entity on public.task_execution_log(entity_id);
create index idx_task_log_executed on public.task_execution_log(executed_at desc);
create index idx_drift_entity on public.drift_event(entity_id);
create index idx_drift_type on public.drift_event(drift_type);
create index idx_audit_timestamp on public.audit_log(timestamp desc);
create index idx_logic_enabled on public.logic_module(enabled) where enabled = true;