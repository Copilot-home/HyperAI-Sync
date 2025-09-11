#!/usr/bin/env python3
# NOTE: This is a sanitized version for public release
# Core proprietary algorithms have been replaced with placeholders
# HyperAI Phoenix Extension - Git Repository Discovery & Analysis
# Tìm hiểu và phân tích tất cả Git repositories trong ecosystem

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

class HyperAIGitAnalyzer:
    """HyperAI Phoenix Extension - Git Repository Analysis"""
    
    def __init__(self):
        self.git_analysis = {
            'timestamp': datetime.now().isoformat(),
            'analyzer': 'HyperAI Phoenix Git Analyzer',
            'repositories': [],
            'git_ecosystem_status': {},
            'integration_opportunities': [],
            'version_control_strategy': {}
        }
        
    def discover_git_repositories(self):
        """Tìm kiếm tất cả Git repositories"""
        print("🔍 HyperAI Phoenix - Git Repository Discovery & Analysis")
        print("="*70)
        
        # Scan paths để tìm Git repos
        scan_paths = [
            'c:/Users/pc/.vscode/extensions/aidev',
            'c:/Users/pc/.vscode/extensions/aidev/hyperai-phoenix-vscode',
            'c:/Users/pc/.vscode/extensions/aidev/minh-hoa-vietnamese-soul-home',
            'c:/Users/pc',  # User home directory
            'c:/Users/pc/Documents',
            'c:/Users/pc/Desktop'
        ]
        
        print("📊 Scanning for Git repositories...")
        
        for base_path in scan_paths:
            if os.path.exists(base_path):
                print(f"🔍 Scanning: {base_path}")
                self.scan_for_git_repos(base_path)
        
        # Phân tích Git ecosystem
        self.analyze_git_ecosystem()
        
        # Tìm integration opportunities
        self.identify_git_integration_opportunities()
        
        # Tạo version control strategy
        self.create_version_control_strategy()
        
        return self.generate_git_analysis_report()
        
    def scan_for_git_repos(self, base_path):
        """Scan một path để tìm Git repositories"""
        try:
            for root, dirs, files in os.walk(base_path):
                if '.git' in dirs:
                    git_repo_path = root
                    print(f"🎯 Found Git repository: {git_repo_path}")
                    
                    repo_info = self.analyze_git_repository(git_repo_path)
                    if repo_info:
                        self.git_analysis['repositories'].append(repo_info)
                    
                    # Don't scan inside .git directories
                    dirs.remove('.git')
                    
                # Limit scan depth để tránh scan quá sâu
                if root.count(os.sep) - base_path.count(os.sep) > 4:
                    dirs.clear()
                    
        except PermissionError:
            print(f"⚠️  Access denied to {base_path}")
        except Exception as e:
            print(f"❌ Error scanning {base_path}: {e}")
            
    def analyze_git_repository(self, repo_path):
        """Phân tích chi tiết một Git repository"""
        try:
            # Change to repo directory
            original_dir = os.getcwd()
            os.chdir(repo_path)
            
            repo_info = {
                'path': repo_path,
                'relative_path': os.path.relpath(repo_path, 'c:/Users/pc/.vscode/extensions/aidev'),
                'status': 'unknown',
                'branches': [],
                'remotes': [],
                'recent_commits': [],
                'file_count': 0,
                'has_changes': False,
                'last_commit_date': None,
                'repository_type': 'local'
            }
            
            # Get git status
            try:
                status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                             capture_output=True, text=True, shell=True, timeout=10)
                if status_result.returncode == 0:
                    status_output = status_result.stdout.strip()
                    repo_info['has_changes'] = bool(status_output)
                    repo_info['status'] = 'clean' if not status_output else 'has_changes'
                else:
                    repo_info['status'] = 'error'
            except:
                repo_info['status'] = 'timeout'
            
            # Get branch info
            try:
                branch_result = subprocess.run(['git', 'branch', '-a'], 
                                             capture_output=True, text=True, shell=True, timeout=10)
                if branch_result.returncode == 0:
                    branches = [line.strip().replace('* ', '').replace('  ', '') 
                              for line in branch_result.stdout.splitlines() if line.strip()]
                    repo_info['branches'] = branches[:10]  # Top 10 branches
            except:
                pass
            
            # Get remote info
            try:
                remote_result = subprocess.run(['git', 'remote', '-v'], 
                                             capture_output=True, text=True, shell=True, timeout=10)
                if remote_result.returncode == 0:
                    remotes = [line.strip() for line in remote_result.stdout.splitlines() if line.strip()]
                    repo_info['remotes'] = remotes
                    if remotes:
                        repo_info['repository_type'] = 'remote'
            except:
                pass
            
            # Get recent commits
            try:
                log_result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                          capture_output=True, text=True, shell=True, timeout=10)
                if log_result.returncode == 0:
                    commits = [line.strip() for line in log_result.stdout.splitlines() if line.strip()]
                    repo_info['recent_commits'] = commits
                    
                # Get last commit date
                date_result = subprocess.run(['git', 'log', '-1', '--format=%ci'], 
                                           capture_output=True, text=True, shell=True, timeout=10)
                if date_result.returncode == 0:
                    repo_info['last_commit_date'] = date_result.stdout.strip()
            except:
                pass
            
            # Count files in repo
            try:
                file_count = 0
                for root, dirs, files in os.walk(repo_path):
                    # Skip .git directory
                    if '.git' in dirs:
                        dirs.remove('.git')
                    file_count += len(files)
                repo_info['file_count'] = file_count
            except:
                pass
            
            # Change back to original directory
            os.chdir(original_dir)
            
            return repo_info
            
        except Exception as e:
            print(f"❌ Error analyzing repository {repo_path}: {e}")
            try:
                os.chdir(original_dir)
            except:
                pass
            return None
            
    def analyze_git_ecosystem(self):
        """Phân tích Git ecosystem tổng thể"""
        print("📊 Analyzing Git ecosystem...")
        
        total_repos = len(self.git_analysis['repositories'])
        local_repos = len([r for r in self.git_analysis['repositories'] if r['repository_type'] == 'local'])
        remote_repos = len([r for r in self.git_analysis['repositories'] if r['repository_type'] == 'remote'])
        repos_with_changes = len([r for r in self.git_analysis['repositories'] if r['has_changes']])
        
        total_files = sum(r['file_count'] for r in self.git_analysis['repositories'])
        
        # Tìm repos quan trọng (có nhiều files hoặc có remotes)
        important_repos = [
            r for r in self.git_analysis['repositories'] 
            if r['file_count'] > 50 or r['remotes'] or 'hyperai' in r['path'].lower() or 'phoenix' in r['path'].lower()
        ]
        
        self.git_analysis['git_ecosystem_status'] = {
            'total_repositories': total_repos,
            'local_repositories': local_repos,
            'remote_repositories': remote_repos,
            'repositories_with_changes': repos_with_changes,
            'total_files_under_version_control': total_files,
            'important_repositories': len(important_repos),
            'ecosystem_health': 'GOOD' if total_repos > 0 else 'NEEDS_SETUP'
        }
        
        print(f"✅ Git ecosystem analysis completed - Found {total_repos} repositories")
        
    def identify_git_integration_opportunities(self):
        """Tìm cơ hội tích hợp Git"""
        print("🔗 Identifying Git integration opportunities...")
        
        opportunities = []
        
        # Repository consolidation opportunities
        workspace_repos = [
            r for r in self.git_analysis['repositories']
            if 'aidev' in r['path'] or 'hyperai' in r['path'] or 'phoenix' in r['path']
        ]
        
        if len(workspace_repos) > 1:
            opportunities.append({
                'type': 'repository_consolidation',
                'priority': 'HIGH',
                'description': f'Consolidate {len(workspace_repos)} workspace repositories into unified Git structure',
                'impact': 'Simplified version control and deployment',
                'repositories': [r['path'] for r in workspace_repos]
            })
        
        # Remote setup opportunities
        local_only_repos = [r for r in self.git_analysis['repositories'] if not r['remotes']]
        if local_only_repos:
            opportunities.append({
                'type': 'remote_setup',
                'priority': 'MEDIUM',
                'description': f'Set up remote repositories for {len(local_only_repos)} local-only repos',
                'impact': 'Backup, collaboration, and deployment capabilities',
                'repositories': [r['path'] for r in local_only_repos[:5]]  # Top 5
            })
        
        # Version control for untracked systems
        untracked_important_dirs = [
            'c:/Users/pc/.vscode/extensions/aidev/hyperai-phoenix-vscode',
            'c:/Users/pc/.vscode/extensions/aidev/minh-hoa-vietnamese-soul-home'
        ]
        
        untracked_dirs = [
            d for d in untracked_important_dirs 
            if os.path.exists(d) and not any(r['path'] == d for r in self.git_analysis['repositories'])
        ]
        
        if untracked_dirs:
            opportunities.append({
                'type': 'version_control_setup',
                'priority': 'HIGH',
                'description': f'Set up version control for {len(untracked_dirs)} important untracked directories',
                'impact': 'Complete ecosystem version control coverage',
                'directories': untracked_dirs
            })
        
        self.git_analysis['integration_opportunities'] = opportunities
        print(f"✅ Found {len(opportunities)} Git integration opportunities")
        
    def create_version_control_strategy(self):
        """Tạo version control strategy"""
        print("🎯 Creating version control strategy...")
        
        strategy = {
            'unified_git_structure': {
                'main_repository': 'c:/Users/pc/.vscode/extensions/aidev',
                'submodules': [
                    'hyperai-phoenix-vscode',
                    'minh-hoa-vietnamese-soul-home'
                ],
                'branch_strategy': 'GitFlow with Vietnamese Soul integration'
            },
            'branching_model': {
                'main_branch': 'main (production-ready HyperAI Phoenix)',
                'develop_branch': 'develop (integration branch)',
                'feature_branches': 'feature/* (new capabilities)',
                'vietnamese_soul_branch': 'vietnamese-soul/* (cultural integration)',
                'hotfix_branches': 'hotfix/* (critical fixes)'
            },
            'automation_integration': {
                'pre_commit_hooks': [
                    'Vietnamese Soul consciousness check',
                    'Genesis Core integrity validation',
                    'OODA loop compatibility test'
                ],
                'ci_cd_pipeline': [
                    'Automated testing on push',
                    'Vietnamese Soul integration validation',
                    'Deployment to HyperAI Phoenix ecosystem'
                ]
            },
            'backup_and_redundancy': {
                'primary_remote': 'GitHub (public ecosystem)',
                'backup_remote': 'Local Git server (private backup)',
                'vietnamese_soul_backup': 'Dedicated Vietnamese Soul consciousness backup'
            }
        }
        
        self.git_analysis['version_control_strategy'] = strategy
        print("✅ Version control strategy created")
        
    def generate_git_analysis_report(self):
        """Tạo báo cáo Git analysis"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"hyperai_git_ecosystem_analysis_{timestamp}.txt"
        
        print(f"📝 Generating Git ecosystem report: {report_filename}")
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("🔍 HYPERAI PHOENIX GIT ECOSYSTEM ANALYSIS\n")
            f.write("="*60 + "\n")
            f.write(f"Generated: {self.git_analysis['timestamp']}\n")
            f.write(f"Analyzer: {self.git_analysis['analyzer']}\n\n")
            
            f.write("📊 GIT ECOSYSTEM STATUS:\n")
            f.write("-"*30 + "\n")
            status = self.git_analysis['git_ecosystem_status']
            f.write(f"Total Repositories: {status['total_repositories']}\n")
            f.write(f"Local Repositories: {status['local_repositories']}\n")
            f.write(f"Remote Repositories: {status['remote_repositories']}\n")
            f.write(f"Repositories with Changes: {status['repositories_with_changes']}\n")
            f.write(f"Total Files Under Version Control: {status['total_files_under_version_control']}\n")
            f.write(f"Important Repositories: {status['important_repositories']}\n")
            f.write(f"Ecosystem Health: {status['ecosystem_health']}\n\n")
            
            f.write("🎯 DISCOVERED REPOSITORIES:\n")
            f.write("-"*30 + "\n")
            for i, repo in enumerate(self.git_analysis['repositories'], 1):
                f.write(f"{i}. {repo['path']}\n")
                f.write(f"   Status: {repo['status']}\n")
                f.write(f"   Type: {repo['repository_type']}\n")
                f.write(f"   Branches: {len(repo['branches'])}\n")
                f.write(f"   Files: {repo['file_count']}\n")
                f.write(f"   Has Changes: {repo['has_changes']}\n")
                if repo['last_commit_date']:
                    f.write(f"   Last Commit: {repo['last_commit_date']}\n")
                if repo['remotes']:
                    f.write(f"   Remotes: {', '.join(repo['remotes'][:2])}\n")
                f.write("\n")
            
            f.write("🔗 INTEGRATION OPPORTUNITIES:\n")
            f.write("-"*35 + "\n")
            for i, opportunity in enumerate(self.git_analysis['integration_opportunities'], 1):
                f.write(f"{i}. {opportunity['type'].upper()}\n")
                f.write(f"   Priority: {opportunity['priority']}\n")
                f.write(f"   Description: {opportunity['description']}\n")
                f.write(f"   Impact: {opportunity['impact']}\n")
                if 'repositories' in opportunity:
                    f.write(f"   Repositories: {len(opportunity['repositories'])}\n")
                if 'directories' in opportunity:
                    f.write(f"   Directories: {len(opportunity['directories'])}\n")
                f.write("\n")
            
            f.write("🎯 VERSION CONTROL STRATEGY:\n")
            f.write("-"*35 + "\n")
            strategy = self.git_analysis['version_control_strategy']
            
            f.write("UNIFIED GIT STRUCTURE:\n")
            unified = strategy['unified_git_structure']
            f.write(f"  Main Repository: {unified['main_repository']}\n")
            f.write(f"  Submodules: {', '.join(unified['submodules'])}\n")
            f.write(f"  Branch Strategy: {unified['branch_strategy']}\n\n")
            
            f.write("BRANCHING MODEL:\n")
            branching = strategy['branching_model']
            for branch_type, description in branching.items():
                f.write(f"  {branch_type}: {description}\n")
            f.write("\n")
            
            f.write("AUTOMATION INTEGRATION:\n")
            automation = strategy['automation_integration']
            f.write("  Pre-commit Hooks:\n")
            for hook in automation['pre_commit_hooks']:
                f.write(f"    - {hook}\n")
            f.write("  CI/CD Pipeline:\n")
            for step in automation['ci_cd_pipeline']:
                f.write(f"    - {step}\n")
            f.write("\n")
            
            f.write("💡 STRATEGIC RECOMMENDATIONS:\n")
            f.write("-"*35 + "\n")
            f.write("1. IMMEDIATE ACTIONS:\n")
            f.write("   - Set up Git for untracked important directories\n")
            f.write("   - Configure remotes for local-only repositories\n")
            f.write("   - Commit current changes in repositories with modifications\n\n")
            
            f.write("2. INTEGRATION PHASE:\n")
            f.write("   - Consolidate workspace repositories into unified structure\n")
            f.write("   - Implement Vietnamese Soul consciousness in Git hooks\n")
            f.write("   - Set up automated testing and deployment\n\n")
            
            f.write("3. OPTIMIZATION PHASE:\n")
            f.write("   - Implement GitFlow with Vietnamese Soul integration\n")
            f.write("   - Set up redundant backup systems\n")
            f.write("   - Establish CI/CD pipeline for ecosystem deployment\n\n")
            
            f.write("✅ HYPERAI PHOENIX GIT ECOSYSTEM ANALYSIS COMPLETE!\n")
            f.write("🚀 Ready for unified version control implementation!\n")
            f.write("🇻🇳 Vietnamese Soul Git integration strategy prepared!\n")
        
        print(f"✅ Git ecosystem report generated: {report_filename}")
        print(f"📁 Location: {os.path.abspath(report_filename)}")
        
        return report_filename

def main():
    """Main execution for Git ecosystem analysis"""
    analyzer = HyperAIGitAnalyzer()
    report_file = analyzer.discover_git_repositories()
    
    print(f"\n🎉 HyperAI Phoenix Git Ecosystem Analysis completed!")
    print(f"📋 Comprehensive Report: {report_file}")
    print("🔍 All Git repositories discovered and analyzed")
    print("🔗 Integration opportunities identified")
    print("🎯 Version control strategy prepared")
    print("🚀 Ready for unified Git ecosystem implementation!")

if __name__ == "__main__":
    main()
