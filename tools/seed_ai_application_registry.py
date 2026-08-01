#!/usr/bin/env python3
"""Seed /Users/andy/HyperAI-Sync/memory/ai_application_registry.db
from verified local sources: Docker MCP catalog, Docker runtime, native AI apps,
LM Studio, OpenAPI tool servers, APΩ aliases, and Claude Desktop MCP clients.
"""

import json
import os
import re
import sqlite3
import subprocess
import datetime
from pathlib import Path

HOME = Path(os.path.expanduser("~"))
WORKSPACE = HOME / "HyperAI-Sync"
OUT_DB = WORKSPACE / "memory" / "ai_application_registry.db"

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()

def run_json(cmd):
    out = run(cmd)
    return [json.loads(line) for line in out.splitlines() if line.strip()]

def did(type_, slug):
    safe = re.sub(r"[^a-zA-Z0-9_.\-:]+", "-", slug).strip("-").lower()[:80]
    return f"did:hyperai:{type_}:{safe}"

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def jsonb(obj):
    return json.dumps(obj, ensure_ascii=False, default=str)

# ------------------------------------------------------------------
# 1. Docker MCP catalog (mcp-toolkit.db)
# ------------------------------------------------------------------
MCP_DB = HOME / ".docker" / "mcp" / "mcp-toolkit.db"

catalog_servers = []
if MCP_DB.exists():
    with sqlite3.connect(MCP_DB) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT id, server_type, image, endpoint, catalog_ref, snapshot FROM catalog_server").fetchall()
        for r in rows:
            snap = json.loads(r["snapshot"] or "{}")
            s = snap.get("server", {})
            meta = s.get("metadata", {})
            tools = s.get("tools", [])
            app = {
                "did": did("mcp", s.get("name") or r["id"]),
                "name": s.get("name") or f"catalog-{r['id']}",
                "display_title": s.get("title") or s.get("name") or f"Catalog {r['id']}",
                "type": "mcp_catalog",
                "subtype": r["server_type"],
                "source": r["server_type"],
                "source_uri": s.get("image") or r["image"] or r["endpoint"],
                "status": "catalog",
                "endpoint": r["endpoint"] or (s.get("remote", {}).get("url")),
                "port": None,
                "description": (s.get("description") or "")[:500],
                "icon": s.get("icon"),
                "tools_json": jsonb([{"name": t.get("name"), "description": (t.get("description") or "")[:200]} for t in tools]),
                "tools_count": len(tools),
                "metadata_json": jsonb(meta),
                "tags_json": jsonb(meta.get("tags", [])),
                "catalog_ref": r["catalog_ref"],
                "image": s.get("image") or r["image"],
                "bundle_id": None,
                "container_id": None,
                "profile": None,
                "created_at": now(),
            }
            catalog_servers.append(app)

# profile memberships
profile_members = {}
if MCP_DB.exists():
    with sqlite3.connect(MCP_DB) as conn:
        conn.row_factory = sqlite3.Row
        ws = conn.execute("SELECT id, name, servers FROM working_set").fetchall()
        for w in ws:
            servers = json.loads(w["servers"] or "[]")
            for s in servers:
                img = s.get("image")
                name = s.get("snapshot", {}).get("server", {}).get("name")
                if not name and img:
                    # parse image ref
                    name = img.split("/")[-1].split("@")[0].split(":")[0]
                key = img or name
                profile_members.setdefault(key, []).append(w["name"])

# attach profile membership to catalog servers
for app in catalog_servers:
    key = app["image"] or app["name"]
    matched = profile_members.get(key, [])
    if not matched:
        # try by name only
        matched = [p for p, lst in profile_members.items() if any(app["name"] in x or x in app["name"] for x in lst)]
    app["profile"] = jsonb(matched) if matched else None

# ------------------------------------------------------------------
# 2. Native AI apps (library_inventory)
# ------------------------------------------------------------------
native_apps = []
INV = HOME / ".apo" / "gateway" / "library_inventory.json"
if INV.exists():
    inv = json.loads(INV.read_text())
    for app_name in inv.get("library", {}).get("ai_apps_in_Application_Support", []):
        slug = app_name.lower().replace(" ", "-").replace("/", "-")
        native_apps.append({
            "did": did("native", slug),
            "name": slug,
            "display_title": app_name,
            "type": "native_app",
            "subtype": "macos_app",
            "source": "installed",
            "source_uri": f"/Users/andy/Library/Application Support/{app_name}",
            "status": "installed",
            "endpoint": None,
            "port": None,
            "description": None,
            "icon": None,
            "tools_json": None,
            "tools_count": 0,
            "metadata_json": jsonb({"bundle_dir": f"/Users/andy/Library/Application Support/{app_name}"}),
            "tags_json": None,
            "catalog_ref": None,
            "image": None,
            "bundle_id": None,
            "container_id": None,
            "profile": None,
            "created_at": now(),
        })

# LM Studio special probe
lm_port_open = False
import socket
try:
    s = socket.socket(); s.settimeout(2); s.connect(("127.0.0.1", 1234)); lm_port_open = True; s.close()
except Exception: pass
lm_bundle = "ai.elementlabs.lmstudio"
lm_version = "0.4.20+1"
lm_status = "running_api_closed" if not lm_port_open else "running_api_open"
lm_app = next((a for a in native_apps if a["name"] == "lm-studio"), None)
if lm_app:
    lm_app["status"] = lm_status
    lm_app["port"] = 1234
    lm_app["endpoint"] = "http://127.0.0.1:1234/v1"
    lm_app["bundle_id"] = lm_bundle
    lm_app["metadata_json"] = jsonb({"bundle_id": lm_bundle, "version": lm_version, "port_open": lm_port_open})

# ------------------------------------------------------------------
# 3. Docker containers, images, volumes, networks
# ------------------------------------------------------------------
def docker_json(cmd):
    try:
        return run_json(cmd)
    except Exception:
        return []

docker_apps = []
containers = docker_json("docker ps -a --format json")
images = docker_json("docker images -a --format json")
volumes = docker_json("docker volume ls --format json")
networks = docker_json("docker network ls --format json")

for c in containers:
    name = c.get("Names", "unknown")
    ports = c.get("Ports", "")
    port = None
    if ports and "->" in ports:
        try:
            port = int(ports.split("->")[0].split(":")[-1])
        except Exception:
            pass
    docker_apps.append({
        "did": did("container", name),
        "name": name,
        "display_title": name,
        "type": "container",
        "subtype": "docker",
        "source": "docker",
        "source_uri": c.get("Image"),
        "status": c.get("State"),
        "endpoint": f"127.0.0.1:{port}" if port else None,
        "port": port,
        "description": f"Docker container {c.get('Status')}",
        "icon": None,
        "tools_json": None,
        "tools_count": 0,
        "metadata_json": jsonb(c),
        "tags_json": jsonb(c.get("Labels", "").split(",") if c.get("Labels") else []),
        "catalog_ref": None,
        "image": c.get("Image"),
        "bundle_id": None,
        "container_id": c.get("ID"),
        "profile": None,
        "created_at": now(),
    })

for img in images:
    repo = img.get("Repository", "<none>")
    tag = img.get("Tag", "<none>")
    name = f"{repo}:{tag}" if repo != "<none>" else img.get("ID", "image")
    docker_apps.append({
        "did": did("image", name),
        "name": name,
        "display_title": name,
        "type": "image",
        "subtype": "docker",
        "source": "docker",
        "source_uri": f"docker.io/{repo}:{tag}" if repo != "<none>" else img.get("ID"),
        "status": img.get("Containers") or "0",
        "endpoint": None,
        "port": None,
        "description": None,
        "icon": None,
        "tools_json": None,
        "tools_count": 0,
        "metadata_json": jsonb(img),
        "tags_json": None,
        "catalog_ref": None,
        "image": name,
        "bundle_id": None,
        "container_id": None,
        "profile": None,
        "created_at": now(),
    })

for vol in volumes:
    name = vol.get("Name", "unknown")
    docker_apps.append({
        "did": did("volume", name),
        "name": name,
        "display_title": name[:40],
        "type": "volume",
        "subtype": "docker",
        "source": "docker",
        "source_uri": vol.get("Mountpoint"),
        "status": "present",
        "endpoint": None,
        "port": None,
        "description": f"Docker volume driver={vol.get('Driver')}",
        "icon": None,
        "tools_json": None,
        "tools_count": 0,
        "metadata_json": jsonb(vol),
        "tags_json": None,
        "catalog_ref": None,
        "image": None,
        "bundle_id": None,
        "container_id": None,
        "profile": None,
        "created_at": now(),
    })

for net in networks:
    name = net.get("Name", "unknown")
    docker_apps.append({
        "did": did("network", name),
        "name": name,
        "display_title": name,
        "type": "network",
        "subtype": "docker",
        "source": "docker",
        "source_uri": None,
        "status": net.get("Driver"),
        "endpoint": None,
        "port": None,
        "description": f"Docker network {net.get('Driver')} {net.get('Scope')}",
        "icon": None,
        "tools_json": None,
        "tools_count": 0,
        "metadata_json": jsonb(net),
        "tags_json": None,
        "catalog_ref": None,
        "image": None,
        "bundle_id": None,
        "container_id": None,
        "profile": None,
        "created_at": now(),
    })

# ------------------------------------------------------------------
# 4. OpenAPI tool servers
# ------------------------------------------------------------------
openapi_apps = []
OPENAPI = HOME / "openapi-servers"
if OPENAPI.exists():
    compose = None
    try:
        import yaml
        compose = yaml.safe_load((OPENAPI / "compose.yaml").read_text())
    except Exception:
        pass
    for srv in sorted((OPENAPI / "servers").iterdir()):
        if not srv.is_dir():
            continue
        name = srv.name
        port = None
        if compose and "services" in compose:
            for svc, cfg in compose["services"].items():
                if svc.startswith(name) or svc == name or name in svc:
                    ports = cfg.get("ports", [])
                    if ports:
                        try:
                            port = int(str(ports[0]).split(":")[0])
                        except Exception:
                            pass
        readme = (srv / "README.md").exists()
        openapi_apps.append({
            "did": did("openapi", name),
            "name": name,
            "display_title": name.replace("-", " ").title(),
            "type": "openapi_server",
            "subtype": "python_uvicorn",
            "source": "local_repo",
            "source_uri": str(srv),
            "status": "configured",
            "endpoint": f"http://127.0.0.1:{port}" if port else None,
            "port": port,
            "description": f"OpenAPI tool server in {srv.name}; README={readme}",
            "icon": None,
            "tools_json": None,
            "tools_count": 0,
            "metadata_json": jsonb({"path": str(srv), "readme": readme, "compose_service": name}),
            "tags_json": None,
            "catalog_ref": None,
            "image": None,
            "bundle_id": None,
            "container_id": None,
            "profile": None,
            "created_at": now(),
        })

# ------------------------------------------------------------------
# 5. APΩ config: aliases, upstreams, tools
# ------------------------------------------------------------------
apo_apps = []
APO_CFG = HOME / ".apo" / "gateway" / "apo_config.yaml"
if APO_CFG.exists():
    import yaml
    cfg = yaml.safe_load(APO_CFG.read_text())

    # aliases
    for alias, data in cfg.get("aliases", {}).items():
        apo_apps.append({
            "did": did("alias", alias),
            "name": alias,
            "display_title": alias,
            "type": "model_alias",
            "subtype": "apΩ_alias",
            "source": "apΩ_config",
            "source_uri": str(APO_CFG),
            "status": "configured",
            "endpoint": None,
            "port": None,
            "description": f"Alias {alias} -> {data.get('upstream')}/{data.get('model')}",
            "icon": None,
            "tools_json": None,
            "tools_count": 0,
            "metadata_json": jsonb(data),
            "tags_json": None,
            "catalog_ref": None,
            "image": None,
            "bundle_id": None,
            "container_id": None,
            "profile": None,
            "created_at": now(),
        })

    # upstreams
    for up, data in cfg.get("upstreams", {}).items():
        apo_apps.append({
            "did": did("upstream", up),
            "name": up,
            "display_title": up,
            "type": "model_upstream",
            "subtype": data.get("type", "openai"),
            "source": "apΩ_config",
            "source_uri": data.get("base_url"),
            "status": "configured",
            "endpoint": data.get("base_url"),
            "port": None,
            "description": f"Upstream {up} at {data.get('base_url')}",
            "icon": None,
            "tools_json": None,
            "tools_count": 0,
            "metadata_json": jsonb(data),
            "tags_json": None,
            "catalog_ref": None,
            "image": None,
            "bundle_id": None,
            "container_id": None,
            "profile": None,
            "created_at": now(),
        })

    # tools
    for tool, data in cfg.get("tools", {}).items():
        port = None
        try:
            port = int(data.get("base_url", "").split(":")[-1])
        except Exception:
            pass
        apo_apps.append({
            "did": did("apotools", tool),
            "name": tool,
            "display_title": tool,
            "type": "apΩ_tool",
            "subtype": "openapi_tool_proxy",
            "source": "apΩ_config",
            "source_uri": data.get("base_url"),
            "status": "configured",
            "endpoint": data.get("base_url"),
            "port": port,
            "description": f"APΩ tool proxy {tool}",
            "icon": None,
            "tools_json": None,
            "tools_count": 0,
            "metadata_json": jsonb(data),
            "tags_json": None,
            "catalog_ref": None,
            "image": None,
            "bundle_id": None,
            "container_id": None,
            "profile": None,
            "created_at": now(),
        })

# ------------------------------------------------------------------
# 6. Claude Desktop MCP clients
# ------------------------------------------------------------------
claude_apps = []
CLAUDE_CFG = HOME / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
if CLAUDE_CFG.exists():
    cc = json.loads(CLAUDE_CFG.read_text())
    mcp = cc.get("mcpServers", {})
    for name, data in mcp.items():
        cmd = data.get("command", "")
        args = data.get("args", [])
        source = " ".join([cmd] + args) if args else cmd
        claude_apps.append({
            "did": did("mcp_client", name),
            "name": name,
            "display_title": name,
            "type": "mcp_client",
            "subtype": "claude_desktop",
            "source": "claude_config",
            "source_uri": str(CLAUDE_CFG),
            "status": "configured",
            "endpoint": None,
            "port": None,
            "description": f"Claude Desktop MCP server: {source}",
            "icon": None,
            "tools_json": None,
            "tools_count": 0,
            "metadata_json": jsonb(data),
            "tags_json": None,
            "catalog_ref": None,
            "image": None,
            "bundle_id": None,
            "container_id": None,
            "profile": None,
            "created_at": now(),
        })

# ------------------------------------------------------------------
# 7. Docker daemon / context
# ------------------------------------------------------------------
docker_info = {}
try:
    docker_info = json.loads(run("docker info --format json"))
except Exception:
    pass

docker_daemon_app = {
    "did": did("docker", "daemon"),
    "name": "docker-daemon",
    "display_title": "Docker Desktop",
    "type": "docker_daemon",
    "subtype": "desktop-linux",
    "source": "docker",
    "source_uri": None,
    "status": "running",
    "endpoint": None,
    "port": None,
    "description": f"Docker Desktop {docker_info.get('ServerVersion', '?')} on {docker_info.get('OperatingSystem', '?')}",
    "icon": None,
    "tools_json": None,
    "tools_count": 0,
    "metadata_json": jsonb(docker_info),
    "tags_json": jsonb(["docker_desktop", "container_fabric"]),
    "catalog_ref": None,
    "image": None,
    "bundle_id": None,
    "container_id": None,
    "profile": None,
    "created_at": now(),
}

# ------------------------------------------------------------------
# 8. Write SQLite DB
# ------------------------------------------------------------------
OUT_DB.parent.mkdir(parents=True, exist_ok=True)
if OUT_DB.exists():
    OUT_DB.unlink()

with sqlite3.connect(OUT_DB) as conn:
    conn.execute("""
        CREATE TABLE applications (
            did TEXT PRIMARY KEY,
            name TEXT,
            display_title TEXT,
            type TEXT,
            subtype TEXT,
            source TEXT,
            source_uri TEXT,
            status TEXT,
            endpoint TEXT,
            port INTEGER,
            description TEXT,
            icon TEXT,
            tools_json TEXT,
            tools_count INTEGER,
            metadata_json TEXT,
            tags_json TEXT,
            catalog_ref TEXT,
            image TEXT,
            bundle_id TEXT,
            container_id TEXT,
            profile TEXT,
            created_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE provenance (
            id INTEGER PRIMARY KEY,
            did TEXT,
            source_file TEXT,
            source_type TEXT,
            extracted_at TEXT
        )
    """)
    conn.execute("CREATE INDEX idx_type ON applications(type)")
    conn.execute("CREATE INDEX idx_status ON applications(status)")
    conn.execute("CREATE INDEX idx_profile ON applications(profile)")

    all_apps = catalog_servers + native_apps + docker_apps + openapi_apps + apo_apps + claude_apps + [docker_daemon_app]

    cols = [
        "did", "name", "display_title", "type", "subtype", "source", "source_uri",
        "status", "endpoint", "port", "description", "icon", "tools_json", "tools_count",
        "metadata_json", "tags_json", "catalog_ref", "image", "bundle_id", "container_id",
        "profile", "created_at"
    ]
    placeholders = ",".join("?" * len(cols))
    insert_sql = f"INSERT INTO applications ({','.join(cols)}) VALUES ({placeholders})"

    for app in all_apps:
        conn.execute(insert_sql, [app.get(c) for c in cols])

    # provenance rows
    prov = [
        (did("mcp", "catalog"), str(MCP_DB), "sqlite"),
        (did("native", "library"), str(INV), "json"),
        (did("container", "docker"), "docker ps/images/volumes/networks --format json", "cli"),
        (did("openapi", "servers"), str(OPENAPI), "dir"),
        (did("alias", "apo"), str(APO_CFG), "yaml"),
        (did("mcp_client", "claude"), str(CLAUDE_CFG), "json"),
    ]
    for d, src, st in prov:
        conn.execute("INSERT INTO provenance (did, source_file, source_type, extracted_at) VALUES (?,?,?,?)", (d, src, st, now()))

    # summary
    counts = {}
    for app in all_apps:
        counts[app["type"]] = counts.get(app["type"], 0) + 1
    conn.execute("""
        CREATE TABLE registry_meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    conn.execute("INSERT INTO registry_meta VALUES (?,?)", ("created_at", now()))
    conn.execute("INSERT INTO registry_meta VALUES (?,?)", ("counts", jsonb(counts)))
    conn.execute("INSERT INTO registry_meta VALUES (?,?)", ("total_applications", str(len(all_apps))))

print(OUT_DB)
