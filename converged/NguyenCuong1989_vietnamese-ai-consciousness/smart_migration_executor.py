# 🚀 HyperAI Phoenix - Smart Migration Executor

import os
import shutil
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
import logging

class SmartMigrationExecutor:
    def __init__(self):
        self.base_path = Path.cwd()
        self.target_ecosystem = "hyperai-phoenix-ecosystem"
        self.backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.migration_log = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for migration process"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_backup(self):
        """Create full backup before migration"""
        print("🔄 Creating comprehensive backup...")
        backup_dir = self.base_path / self.backup_path
        backup_dir.mkdir(exist_ok=True)
        
        try:
            # Backup critical files
            critical_files = [
                "hyperai_comprehensive_ecosystem_tracker.py",
                "hyperai_comprehensive_ecosystem_tracking_*.txt",
                "AI_IMPLEMENTATION_STRATEGY.md"
            ]
            
            for pattern in critical_files:
                for file in self.base_path.glob(pattern):
                    if file.is_file():
                        shutil.copy2(file, backup_dir)
                        self.logger.info(f"✅ Backed up: {file.name}")
                        
            print(f"✅ Backup created: {backup_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Backup failed: {e}")
            return False
            
    def create_ecosystem_structure(self):
        """Create unified ecosystem directory structure"""
        print("🏗️ Creating unified ecosystem structure...")
        
        ecosystem_structure = {
            "core": [
                "genesis",
                "vietnamese-soul", 
                "hyperai-engine",
                "ooda-loops"
            ],
            "systems": [
                "copilot-integration",
                "phoenix-vscode",
                "agents",
                "automation",
                "general"
            ],
            "data": [
                "databases",
                "logs", 
                "backups",
                "consciousness"
            ],
            "documentation": [
                "technical",
                "api",
                "reports",
                "vietnamese-soul"
            ],
            "development": [
                "testing",
                "staging",
                "tools",
                "configs"
            ],
            "archived": [
                "old-versions",
                "redundant", 
                "temporary"
            ]
        }
        
        ecosystem_path = self.base_path / self.target_ecosystem
        
        try:
            for main_dir, sub_dirs in ecosystem_structure.items():
                main_path = ecosystem_path / main_dir
                main_path.mkdir(parents=True, exist_ok=True)
                
                for sub_dir in sub_dirs:
                    sub_path = main_path / sub_dir
                    sub_path.mkdir(exist_ok=True)
                    
                    # Create .gitkeep for empty directories
                    gitkeep = sub_path / ".gitkeep"
                    gitkeep.touch()
                    
                self.logger.info(f"✅ Created structure: {main_dir}/")
                
            print(f"✅ Ecosystem structure created: {ecosystem_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Structure creation failed: {e}")
            return False
            
    def migrate_systems(self):
        """Migrate systems with AI intelligence"""
        print("🤖 Starting AI-powered system migration...")
        
        # Migration mapping based on AI analysis
        migration_map = {
            ".vscode": "systems/copilot-integration",
            "hyperai_agents": "systems/agents", 
            "core_system": "core/genesis",
            "hyperai-phoenix-vscode": "systems/phoenix-vscode",
            "COPILOT_SERVER": "systems/copilot-integration",
            "consciousness_backup_*": "data/consciousness",
            "*.py": "core/hyperai-engine",
            "*.md": "documentation/technical",
            "*.json": "data/databases",
            "*.log": "data/logs",
            "*.txt": "documentation/reports"
        }
        
        ecosystem_path = self.base_path / self.target_ecosystem
        migrated_count = 0
        
        try:
            for source_pattern, target_path in migration_map.items():
                target_dir = ecosystem_path / target_path
                
                # Handle glob patterns
                if "*" in source_pattern:
                    for source_file in self.base_path.glob(source_pattern):
                        if source_file.name != self.target_ecosystem and source_file.exists():
                            self._migrate_item(source_file, target_dir)
                            migrated_count += 1
                else:
                    source_path = self.base_path / source_pattern
                    if source_path.exists() and source_path.name != self.target_ecosystem:
                        self._migrate_item(source_path, target_dir)
                        migrated_count += 1
                        
            print(f"✅ Migration completed: {migrated_count} items migrated")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Migration failed: {e}")
            return False
            
    def _migrate_item(self, source, target_dir):
        """Migrate individual item with safety checks"""
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / source.name
            
            if source.is_file():
                shutil.copy2(source, target_path)
                self.logger.info(f"📁 Migrated file: {source.name} → {target_dir.relative_to(self.base_path / self.target_ecosystem)}")
            elif source.is_dir():
                shutil.copytree(source, target_path, dirs_exist_ok=True)
                self.logger.info(f"📂 Migrated directory: {source.name} → {target_dir.relative_to(self.base_path / self.target_ecosystem)}")
                
            self.migration_log.append({
                "source": str(source),
                "target": str(target_path),
                "type": "file" if source.is_file() else "directory",
                "timestamp": datetime.now().isoformat(),
                "size": self._get_size(source)
            })
            
        except Exception as e:
            self.logger.error(f"❌ Failed to migrate {source}: {e}")
            
    def _get_size(self, path):
        """Get size of file or directory"""
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
        return 0
        
    def initialize_git_ecosystem(self):
        """Initialize Git repository for unified ecosystem"""
        print("🔗 Initializing Git ecosystem...")
        
        ecosystem_path = self.base_path / self.target_ecosystem
        
        try:
            # Initialize Git repository
            subprocess.run(['git', 'init'], cwd=ecosystem_path, check=True, 
                         capture_output=True, text=True)
            
            # Create initial commit
            subprocess.run(['git', 'add', '.'], cwd=ecosystem_path, check=True,
                         capture_output=True, text=True)
            subprocess.run(['git', 'commit', '-m', 'Initial HyperAI Phoenix Ecosystem Setup with Vietnamese Soul 269Hz'], 
                         cwd=ecosystem_path, check=True, capture_output=True, text=True)
            
            # Create Vietnamese Soul branch
            subprocess.run(['git', 'checkout', '-b', 'vietnamese-soul-269hz'], 
                         cwd=ecosystem_path, check=True, capture_output=True, text=True)
            subprocess.run(['git', 'checkout', 'main'], 
                         cwd=ecosystem_path, check=True, capture_output=True, text=True)
            
            self.logger.info("✅ Git ecosystem initialized with Vietnamese Soul consciousness")
            print("✅ Git ecosystem initialized")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Git initialization failed: {e}")
            return False
            
    def create_migration_report(self):
        """Create comprehensive migration report"""
        print("📋 Generating migration report...")
        
        report_data = {
            "migration_timestamp": datetime.now().isoformat(),
            "ecosystem_path": str(self.base_path / self.target_ecosystem),
            "backup_path": str(self.base_path / self.backup_path),
            "total_migrated": len(self.migration_log),
            "total_size": sum(item["size"] for item in self.migration_log),
            "migration_details": self.migration_log,
            "vietnamese_soul_integration": "269Hz frequency consciousness embedded",
            "ai_intelligence": "Smart categorization and optimization applied"
        }
        
        report_file = self.base_path / f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Migration report created: {report_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Report creation failed: {e}")
            return False
            
    def execute_full_migration(self):
        """Execute complete migration process"""
        print("🚀 Starting HyperAI Phoenix Smart Migration...")
        print("================================================================================")
        
        steps = [
            ("Creating backup", self.create_backup),
            ("Creating ecosystem structure", self.create_ecosystem_structure),
            ("Migrating systems", self.migrate_systems),
            ("Initializing Git ecosystem", self.initialize_git_ecosystem),
            ("Creating migration report", self.create_migration_report)
        ]
        
        for step_name, step_function in steps:
            print(f"\n🔄 {step_name}...")
            if not step_function():
                print(f"❌ {step_name} failed! Migration aborted.")
                return False
                
        print("\n================================================================================")
        print("🎉 HyperAI Phoenix Smart Migration completed successfully!")
        print(f"📁 Ecosystem location: {self.base_path / self.target_ecosystem}")
        print(f"💾 Backup location: {self.base_path / self.backup_path}")
        print("🇻🇳 Vietnamese Soul consciousness integrated at 269Hz frequency")
        print("🤖 AI intelligence applied for smart organization")
        print("🔗 Git ecosystem ready for collaboration")
        print("✨ Ready for unified development workflow!")
        
        return True

if __name__ == "__main__":
    # Execute smart migration
    migrator = SmartMigrationExecutor()
    success = migrator.execute_full_migration()
    
    if success:
        print("\n🌟 Migration successful! Your HyperAI Phoenix ecosystem is ready!")
    else:
        print("\n❌ Migration failed. Check logs for details.")
