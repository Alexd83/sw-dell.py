from netmiko import ConnectHandler

# configuração dos switches Dell
switch1 = {
    'device_type': 'dell_os10',
    'ip': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
}

switch2 = {
    'device_type': 'dell_os10',
    'ip': '192.168.1.2',
    'username': 'admin',
    'password': 'password',
}

switches = [switch1, switch2]

# atualização dos switches
for switch in switches:
    # conecta-se ao switch
    with ConnectHandler(**switch) as net_connect:
        # envia o comando para verificar a versão do firmware
        output = net_connect.send_command('show version')

        # extrai a versão atual do firmware do switch
        current_version = output.split('\n')[1].split(':')[1].strip()

        # imprime a versão atual do firmware
        print(f"Switch {switch['ip']} - Versão atual: {current_version}")

        # envia o comando para atualizar o firmware
        output = net_connect.send_command_timing('update bootcode flash:/bootcode_filename.bin')

        # responde às solicitações de confirmação durante a atualização do firmware
        if 'Do you want to proceed' in output:
            output += net_connect.send_command_timing('yes')
        if 'Do you want to continue' in output:
            output += net_connect.send_command_timing('yes')

        # verifica se a atualização foi bem-sucedida
        if 'Update successful' in output:
            print(f"Switch {switch['ip']} - Atualização do firmware concluída com sucesso")
        else:
            print(f"Switch {switch['ip']} - Falha na atualização do firmware")
