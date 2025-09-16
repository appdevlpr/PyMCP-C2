def handle_metasploit_command(self, command_args):
    if command_args[0] == "run_exploit":
        result = self.metasploit_client.run_exploit(command_args[1], command_args[2])
        self.logger.info(f"Exploit executed: {result}")
    elif command_args[0] == "generate_payload":
        payload = self.metasploit_client.generate_payload(command_args[1], command_args[2])
        self.logger.info(f"Payload generated: {payload}")
