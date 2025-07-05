"""
Comprehensive diagnostics script for project health checks.
Checks database connectivity, API status, Docker status, and system resources.
"""

import os
import sys
import subprocess
import requests
import sqlite3
import psutil
from typing import Dict, List, Tuple
import json

class Diagnostics:
    def __init__(self):
        self.results = {}
        self.errors = []
        
    def check_system_resources(self) -> Dict:
        """Check system resources (CPU, memory, disk)"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "status": "OK",
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2)
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}
    
    def check_database_connectivity(self) -> Dict:
        """Check database connectivity (SQLite example)"""
        try:
            # Try to create a test database connection
            conn = sqlite3.connect(':memory:')
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            result = cursor.fetchone()
            conn.close()
            
            return {
                "status": "OK",
                "message": "Database connectivity successful",
                "test_query": result[0]
            }
        except Exception as e:
            return {"status": "ERROR", "message": f"Database connection failed: {str(e)}"}
    
    def check_api_status(self) -> Dict:
        """Check external API status"""
        apis_to_check = [
            {"name": "OpenAI API", "url": "https://api.openai.com/v1/models", "headers": {}},
            {"name": "GitHub API", "url": "https://api.github.com", "headers": {}}
        ]
        
        results = {}
        for api in apis_to_check:
            try:
                response = requests.get(api["url"], headers=api["headers"], timeout=10)
                results[api["name"]] = {
                    "status": "OK" if response.status_code == 200 else "WARNING",
                    "status_code": response.status_code,
                    "response_time_ms": round(response.elapsed.total_seconds() * 1000, 2)
                }
            except Exception as e:
                results[api["name"]] = {
                    "status": "ERROR",
                    "message": str(e)
                }
        
        return results
    
    def check_docker_status(self) -> Dict:
        """Check Docker daemon status"""
        try:
            result = subprocess.run(
                ['docker', 'version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                return {
                    "status": "OK",
                    "message": "Docker daemon is running",
                    "version": result.stdout.split('\n')[0] if result.stdout else "Unknown"
                }
            else:
                return {
                    "status": "ERROR",
                    "message": "Docker daemon is not running or not accessible",
                    "stderr": result.stderr
                }
        except FileNotFoundError:
            return {"status": "ERROR", "message": "Docker is not installed"}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}
    
    def check_environment_variables(self) -> Dict:
        """Check if required environment variables are set"""
        required_vars = ['OPENAI_API_KEY']
        optional_vars = ['DEBUG', 'DATABASE_URL', 'API_BASE_URL']
        
        results = {
            "required": {},
            "optional": {},
            "missing_required": []
        }
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                results["required"][var] = "SET"
            else:
                results["required"][var] = "MISSING"
                results["missing_required"].append(var)
        
        for var in optional_vars:
            value = os.getenv(var)
            results["optional"][var] = "SET" if value else "NOT_SET"
        
        return results
    
    def check_python_environment(self) -> Dict:
        """Check Python environment and dependencies"""
        try:
            # Check Python version
            python_version = sys.version_info
            
            # Try to import common packages
            packages_to_check = ['requests', 'psutil', 'sqlite3']
            package_status = {}
            
            for package in packages_to_check:
                try:
                    __import__(package)
                    package_status[package] = "OK"
                except ImportError:
                    package_status[package] = "MISSING"
            
            return {
                "status": "OK",
                "python_version": f"{python_version.major}.{python_version.minor}.{python_version.micro}",
                "packages": package_status
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}
    
    def run_all_checks(self) -> Dict:
        """Run all diagnostic checks"""
        print("🔍 Running comprehensive diagnostics...")
        print("=" * 50)
        
        checks = {
            "system_resources": self.check_system_resources(),
            "database_connectivity": self.check_database_connectivity(),
            "api_status": self.check_api_status(),
            "docker_status": self.check_docker_status(),
            "environment_variables": self.check_environment_variables(),
            "python_environment": self.check_python_environment()
        }
        
        # Print results
        for check_name, result in checks.items():
            print(f"\n📋 {check_name.replace('_', ' ').title()}:")
            if isinstance(result, dict):
                if result.get("status") == "OK":
                    print(f"   ✅ {result.get('message', 'Check passed')}")
                elif result.get("status") == "WARNING":
                    print(f"   ⚠️  {result.get('message', 'Check warning')}")
                else:
                    print(f"   ❌ {result.get('message', 'Check failed')}")
            else:
                print(f"   📊 {result}")
        
        return checks
    
    def generate_report(self) -> str:
        """Generate a formatted diagnostic report"""
        checks = self.run_all_checks()
        
        report = []
        report.append("# Diagnostic Report")
        report.append(f"Generated at: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}")
        report.append("")
        
        for check_name, result in checks.items():
            report.append(f"## {check_name.replace('_', ' ').title()}")
            report.append(f"```json")
            report.append(json.dumps(result, indent=2))
            report.append("```")
            report.append("")
        
        return "\n".join(report)

def main():
    """Main function to run diagnostics"""
    diagnostics = Diagnostics()
    
    try:
        # Run all checks
        results = diagnostics.run_all_checks()
        
        # Generate and save report
        report = diagnostics.generate_report()
        with open('diagnostic_report.md', 'w') as f:
            f.write(report)
        
        print("\n" + "=" * 50)
        print("📄 Full diagnostic report saved to: diagnostic_report.md")
        
        # Check for critical errors
        critical_errors = []
        for check_name, result in results.items():
            if isinstance(result, dict) and result.get("status") == "ERROR":
                critical_errors.append(f"{check_name}: {result.get('message', 'Unknown error')}")
        
        if critical_errors:
            print("\n❌ Critical errors found:")
            for error in critical_errors:
                print(f"   - {error}")
            sys.exit(1)
        else:
            print("\n✅ All critical checks passed!")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnostics interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during diagnostics: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 