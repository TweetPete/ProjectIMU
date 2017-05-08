import subprocess

cmd = ["C:\plink", "192.168.137.2", "-l", "pi", "-pw", "0wT0fnDy"]
ff=subprocess.Popen(cmd,shell=False,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
ff.stdout = subprocess.PIPE
print('wait fertig')
#ff.stdout.flush()
#ff.stdin.write("date\n".encode())
#ff.stdin.write("command2\n".encode())
#ff.stdin.close()
ans, _ = ff.communicate()
#ff.communicate('date'.encode())

#ff.stdin.flush()
#ff.communicate(input='date'.encode())
#print("output = :",ans.decode())


