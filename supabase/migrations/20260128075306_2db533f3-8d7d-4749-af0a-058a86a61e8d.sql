-- Fix function search_path for security compliance

-- 1. Fix forbid_identity_update
create or replace function public.forbid_identity_update()
returns trigger 
language plpgsql
security definer
set search_path = public
as $$
begin
    raise exception 'IDENTITY_IMMUTABLE: Cannot modify or delete identity records';
end;
$$;

-- 2. Fix create_identity_state
create or replace function public.create_identity_state()
returns trigger 
language plpgsql
security definer
set search_path = public
as $$
begin
    insert into public.identity_state (entity_id, state, variance_score)
    values (new.entity_id, 'NO_IDENTITY', 1.0);
    return new;
end;
$$;

-- 3. Fix save_logic_version
create or replace function public.save_logic_version()
returns trigger 
language plpgsql
security definer
set search_path = public
as $$
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
$$;

-- 4. Fix classify_drift
create or replace function public.classify_drift()
returns trigger 
language plpgsql
security definer
set search_path = public
as $$
begin
    if new.logic_id is not null then
        new.drift_type := 'SYSTEMIC';
    else
        new.drift_type := 'PER_NODE';
    end if;
    return new;
end;
$$;