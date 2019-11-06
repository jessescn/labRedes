import subprocess

output = ['iperf', '-c', '0.0.0.0']
values = subprocess.check_output(output)
print(values)