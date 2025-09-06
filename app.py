from flask import Flask, jsonify, request
import random
import string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Question datasets with topic field added
python_questions = [
    dict(q, topic="python") for q in [
        {"id": 1, "question": "Which of the following is a mutable data type in Python?", "options": ["Tuple", "List", "String"], "answer": "List"},
        {"id": 2, "question": "What is the output of print(type([])) in Python?", "options": ["<class 'list'>", "<class 'dict'>", "<class 'tuple'>"], "answer": "<class 'list'>"},
        {"id": 3, "question": "Which method is used to add an element at the end of a list in Python?", "options": ["append()", "insert()", "add()"], "answer": "append()"},
        {"id": 4, "question": "What is the correct way to create a function in Python?", "options": ["function myFunc():", "def myFunc():", "create myFunc():"], "answer": "def myFunc():"},
        {"id": 5, "question": "Which of the following is not a valid variable name in Python?", "options": ["_myvar", "my-var", "myvar2"], "answer": "my-var"},
        {"id": 6, "question": "What is the purpose of the 'self' keyword in Python?", "options": ["To refer to the current instance of a class", "To refer to the parent class", "To create a new instance"], "answer": "To refer to the current instance of a class"},
        {"id": 7, "question": "Which of the following is a Python tuple?", "options": ["[1, 2, 3]", "(1, 2, 3)", "1, 2, 3"], "answer": "(1, 2, 3)"},
        {"id": 8, "question": "How do you start a comment in Python?", "options": ["//", "#", "/*"], "answer": "#"},
        {"id": 9, "question": "What is the output of print(2 ** 3) in Python?", "options": ["8", "9", "6"], "answer": "8"},
        {"id": 10, "question": "Which keyword is used to handle exceptions in Python?", "options": ["try", "catch", "finally"], "answer": "try"},
        {"id": 11, "question": "What is the default port number for HTTP?", "options": ["80", "443", "21"], "answer": "80"},
        {"id": 12, "question": "Which of the following is a Python dictionary?", "options": ["{key: value}", "[key: value]", "(key: value)"], "answer": "{key: value}"},
        {"id": 13, "question": "How do you create a virtual environment in Python?", "options": ["python -m venv myenv", "python myenv", "virtualenv myenv"], "answer": "python -m venv myenv"},
        {"id": 14, "question": "Which of the following is a Python set?", "options": ["{1, 2, 3}", "[1, 2, 3]", "(1, 2, 3)"], "answer": "{1, 2, 3}"},
        {"id": 15, "question": "What is the output of print(bool('False')) in Python?", "options": ["True", "False", "None"], "answer": "True"},
        {"id": 16, "question": "Which operator is used to concatenate strings in Python?", "options": ["+", "&", "concat"], "answer": "+"},
        {"id": 17, "question": "What is the purpose of the pass statement in Python?", "options": ["To exit a function", "To do nothing", "To raise an exception"], "answer": "To do nothing"},
        {"id": 18, "question": "Which of the following is a Python keyword?", "options": ["function", "def", "method"], "answer": "def"},
        {"id": 19, "question": "What is the output of print('Hello' + 'World') in Python?", "options": ["Hello World", "HelloWorld", "Error"], "answer": "HelloWorld"},
        {"id": 20, "question": "Which function is used to read a file in Python?", "options": ["open()", "read()", "file()"], "answer": "open()"},
        {"id": 21, "question": "What is the output of print(10 / 2) in Python?", "options": ["5", "5.0", "Error"], "answer": "5.0"},
        {"id": 22, "question": "Which of the following is not a valid Python data type?", "options": ["int", "float", "decimal"], "answer": "decimal"},
        {"id": 23, "question": "What is the purpose of the return statement in a function?", "options": ["To return a value from the function", "To exit the function", "Both a and b"], "answer": "Both a and b"},
        {"id": 24, "question": "Which of the following is a Python loop?", "options": ["for", "while", "repeat"], "answer": "for"},
        {"id": 25, "question": "What is the output of print('2' + 2) in Python?", "options": ["22", "4", "Error"], "answer": "Error"},
        {"id": 26, "question": "Which module is used to work with regular expressions in Python?", "options": ["re", "regex", "regexpr"], "answer": "re"},
        {"id": 27, "question": "What is the purpose of the with statement in Python?", "options": ["To handle exceptions", "To manage file streams", "Both a and b"], "answer": "Both a and b"},
        {"id": 28, "question": "Which of the following is a Python package manager?", "options": ["pip", "setuptools", "wheel"], "answer": "pip"},
        {"id": 29, "question": "What is the output of print(len('Hello')) in Python?", "options": ["5", "4", "Error"], "answer": "5"},
        {"id": 30, "question": "Which of these is the correct file extension for Python files?", "options": [".py", ".python", ".p"], "answer": ".py"}
    ]
]

java_questions = [
    dict(q, topic="java") for q in [
        {"id": 1, "question": "Which keyword is used to inherit a class in Java?", "options": ["inherits", "extends", "implements"], "answer": "extends"},
        {"id": 2, "question": "What is the default value of a boolean variable in Java?", "options": ["true", "false", "0"], "answer": "false"},
        {"id": 3, "question": "Which of the following is not a primitive data type in Java?", "options": ["int", "boolean", "String"], "answer": "String"},
        {"id": 4, "question": "What is the purpose of the 'static' keyword in Java?", "options": ["To define a constant variable", "To create a class method or variable", "Both a and b"], "answer": "Both a and b"},
        {"id": 5, "question": "Which of these is a valid constructor in Java?", "options": ["MyClass()", "MyClass(void)", "MyClass[]"], "answer": "MyClass()"},
        {"id": 6, "question": "What is the output of System.out.println(10 + 20 + '30'); in Java?", "options": ["102030", "1030", "Error"], "answer": "1030"},
        {"id": 7, "question": "Which operator is used to compare two values in Java?", "options": ["=", "==", "==="], "answer": "=="},
        {"id": 8, "question": "What is the purpose of the 'this' keyword in Java?", "options": ["To refer to the current class", "To refer to the current object", "Both a and b"], "answer": "To refer to the current object"},
        {"id": 9, "question": "Which of the following is a valid package statement in Java?", "options": ["package mypackage;", "package: mypackage;", "import mypackage;"], "answer": "package mypackage;"},
        {"id": 10, "question": "What is the output of System.out.println(2 * 3 + 1); in Java?", "options": ["7", "6", "Error"], "answer": "7"},
        {"id": 11, "question": "Which keyword is used to prevent a class from being subclassed in Java?", "options": ["final", "static", "private"], "answer": "final"},
        {"id": 12, "question": "What is the purpose of the super keyword in Java?", "options": ["To call the parent class constructor", "To access parent class methods and variables", "Both a and b"], "answer": "Both a and b"},
        {"id": 13, "question": "Which of these is a valid way to declare an array in Java?", "options": ["int[] arr;", "int arr[];", "Both a and b"], "answer": "Both a and b"},
        {"id": 14, "question": "What is the output of System.out.println('Hello' + 'World'); in Java?", "options": ["Hello World", "HelloWorld", "Error"], "answer": "HelloWorld"},
        {"id": 15, "question": "Which method is used to convert a string to an integer in Java?", "options": ["Integer.parseInt()", "String.toInt()", "Int.valueOf()"], "answer": "Integer.parseInt()"},
        {"id": 16, "question": "What is the purpose of the break statement in Java?", "options": ["To exit a loop or switch statement", "To terminate the program", "Both a and b"], "answer": "To exit a loop or switch statement"},
        {"id": 17, "question": "Which of the following is not a valid way to create a thread in Java?", "options": ["By extending the Thread class", "By implementing the Runnable interface", "By using the Executor framework"], "answer": "By using the Executor framework"},
        {"id": 18, "question": "What is the output of System.out.println(10 == 10.0); in Java?", "options": ["true", "false", "Error"], "answer": "true"},
        {"id": 19, "question": "Which keyword is used to define an interface in Java?", "options": ["interface", "implements", "extends"], "answer": "interface"},
        {"id": 20, "question": "What is the purpose of the synchronized keyword in Java?", "options": ["To create a synchronized block or method", "To define a constant variable", "Both a and b"], "answer": "To create a synchronized block or method"},
        {"id": 21, "question": "Which of these is a valid way to handle exceptions in Java?", "options": ["try-catch", "throws", "try-catch-finally"], "answer": "try-catch-finally"},
        {"id": 22, "question": "What is the output of System.out.println('A' + 1); in Java?", "options": ["A1", "66", "Error"], "answer": "Error"},
        {"id": 23, "question": "Which method is used to get the length of an array in Java?", "options": ["array.length", "array.size()", "array.getSize()"], "answer": "array.length"},
        {"id": 24, "question": "What is the purpose of the volatile keyword in Java?", "options": ["To indicate that a variable may change unexpectedly", "To define a constant variable", "Both a and b"], "answer": "To indicate that a variable may change unexpectedly"},
        {"id": 25, "question": "Which of the following is not a valid Java identifier?", "options": ["_myVar", "myVar2", "2myVar"], "answer": "2myVar"},
        {"id": 26, "question": "What is the output of System.out.println(10 & 3); in Java?", "options": ["2", "3", "1"], "answer": "2"},
        {"id": 27, "question": "Which keyword is used to import a package in Java?", "options": ["import", "include", "using"], "answer": "import"},
        {"id": 28, "question": "What is the purpose of the instanceof operator in Java?", "options": ["To check if an object is an instance of a specific class or subclass", "To compare two objects", "Both a and b"], "answer": "To check if an object is an instance of a specific class or subclass"},
        {"id": 29, "question": "Which of these is a valid way to declare a constant in Java?", "options": ["const int MAX_VALUE;", "final int MAX_VALUE;", "int MAX_VALUE = constant;"], "answer": "final int MAX_VALUE;"},
        {"id": 30, "question": "Which file extension is used for compiled Java bytecode?", "options": [".java", ".class", ".jar"], "answer": ".class"}
    ]
]

c_questions = [
    dict(q, topic="c") for q in [
        {"id": 1, "question": "Which symbol is used to denote a pointer in C?", "options": ["&", "*", "#"], "answer": "*"},
        {"id": 2, "question": "What is the default return type of a function in C?", "options": ["int", "void", "char"], "answer": "int"},
        {"id": 3, "question": "Which of the following is a valid comment in C?", "options": ["// This is a comment", "/* This is a comment */", "# This is a comment"], "answer": "/* This is a comment */"},
        {"id": 4, "question": "What is the purpose of the #include directive in C?", "options": ["To include standard libraries", "To define macros", "Both a and b"], "answer": "Both a and b"},
        {"id": 5, "question": "Which of these is a valid way to declare an array in C?", "options": ["int arr[];", "int[] arr;", "Both a and b"], "answer": "Both a and b"},
        {"id": 6, "question": "What is the output of printf('%d', 10 + 20) in C?", "options": ["30", "1020", "Error"], "answer": "30"},
        {"id": 7, "question": "Which keyword is used to define a macro in C?", "options": ["define", "macro", "const"], "answer": "define"},
        {"id": 8, "question": "What is the purpose of the void keyword in C?", "options": ["To define a function that returns no value", "To define a pointer", "Both a and b"], "answer": "Both a and b"},
        {"id": 9, "question": "Which of the following is not a valid data type in C?", "options": ["int", "float", "decimal"], "answer": "decimal"},
        {"id": 10, "question": "What is the output of printf('%c', 'A' + 1) in C?", "options": ["B", "A", "Error"], "answer": "B"},
        {"id": 11, "question": "Which function is used to read a string in C?", "options": ["gets()", "scanf()", "fgets()"], "answer": "fgets()"},
        {"id": 12, "question": "What is the purpose of the return 0; statement in main() function in C?", "options": ["To return a value to the operating system", "To exit the program", "Both a and b"], "answer": "Both a and b"},
        {"id": 13, "question": "Which of these is a valid way to allocate memory dynamically in C?", "options": ["malloc()", "calloc()", "Both a and b"], "answer": "Both a and b"},
        {"id": 14, "question": "What is the output of printf('%.2f', 3.14159) in C?", "options": ["3.14", "3.1416", "Error"], "answer": "3.14"},
        {"id": 15, "question": "Which of the following is not a valid preprocessor directive in C?", "options": ["#include", "#define", "#ifdef"], "answer": "#ifdef"},
        {"id": 16, "question": "What is the purpose of the static keyword in C?", "options": ["To define a static variable or function", "To create a constant variable", "Both a and b"], "answer": "Both a and b"},
        {"id": 17, "question": "Which of these is a valid way to declare a structure in C?", "options": ["struct myStruct;", "struct myStruct {}", "Both a and b"], "answer": "Both a and b"},
        {"id": 18, "question": "What is the output of printf('%s', 'Hello, World!') in C?", "options": ["Hello, World!", "Error", "Undefined behavior"], "answer": "Hello, World!"},
        {"id": 19, "question": "Which function is used to close a file in C?", "options": ["fclose()", "close()", "end()"], "answer": "fclose()"},
        {"id": 20, "question": "What is the purpose of the const keyword in C?", "options": ["To define a constant value", "To make a variable read-only", "Both a and b"], "answer": "Both a and b"},
        {"id": 21, "question": "Which of these is a valid way to declare an enumeration in C?", "options": ["enum myEnum;", "enum myEnum {}", "Both a and b"], "answer": "Both a and b"},
        {"id": 22, "question": "What is the output of printf('%d', sizeof(int)) in C?", "options": ["4", "2", "Error"], "answer": "4"},
        {"id": 23, "question": "Which keyword is used to define a union in C?", "options": ["union", "struct", "enum"], "answer": "union"},
        {"id": 24, "question": "What is the purpose of the volatile keyword in C?", "options": ["To indicate that a variable may change unexpectedly", "To define a constant variable", "Both a and b"], "answer": "To indicate that a variable may change unexpectedly"},
        {"id": 25, "question": "Which of the following is not a valid way to comment in C?", "options": ["// This is a comment", "/* This is a comment */", "# This is a comment"], "answer": "# This is a comment"},
        {"id": 26, "question": "What is the output of printf('%d', 10 & 3) in C?", "options": ["2", "3", "1"], "answer": "2"},
        {"id": 27, "question": "Which keyword is used to import a header file in C?", "options": ["import", "include", "using"], "answer": "include"},
        {"id": 28, "question": "What is the purpose of the sizeof operator in C?", "options": ["To get the size of a variable or data type", "To define a constant variable", "Both a and b"], "answer": "To get the size of a variable or data type"},
        {"id": 29, "question": "Which of these is a valid way to declare a constant in C?", "options": ["const int MAX_VALUE;", "define MAX_VALUE;", "int MAX_VALUE = constant;"], "answer": "const int MAX_VALUE;"},
        {"id": 30, "question": "Which function is used to compare two strings in C?", "options": ["strcmp()", "strcpy()", "strlen()"], "answer": "strcmp()"}
    ]
]

network_questions = [
    dict(q, topic="network") for q in [
        {"id": 1, "question": "Which device is used to connect multiple networks together?", "options": ["Switch", "Router", "Hub"], "answer": "Router"},
        {"id": 2, "question": "What is the default subnet mask for a Class C network?", "options": ["255.255.255.0", "255.255.0.0", "255.0.0.0"], "answer": "255.255.255.0"},
        {"id": 3, "question": "Which protocol is used to send error messages and operational information?", "options": ["ICMP", "TCP", "UDP"], "answer": "ICMP"},
        {"id": 4, "question": "What is the purpose of the ARP protocol?", "options": ["To resolve IP addresses to MAC addresses", "To route packets between networks", "To establish a secure connection"], "answer": "To resolve IP addresses to MAC addresses"},
        {"id": 5, "question": "Which of the following is a private IP address?", "options": ["192.168.1.1", "172.16.0.1", "Both a and b"], "answer": "Both a and b"},
        {"id": 6, "question": "What is the maximum length of a CAT5e cable?", "options": ["100 meters", "200 meters", "300 meters"], "answer": "100 meters"},
        {"id": 7, "question": "Which layer of the OSI model does the IP protocol operate?", "options": ["Transport", "Network", "Data Link"], "answer": "Network"},
        {"id": 8, "question": "What is the purpose of the DHCP protocol?", "options": ["To assign IP addresses dynamically", "To resolve domain names", "To secure network communications"], "answer": "To assign IP addresses dynamically"},
        {"id": 9, "question": "Which of the following is a characteristic of UDP?", "options": ["Connection-oriented", "Reliable", "Low latency"], "answer": "Low latency"},
        {"id": 10, "question": "What is the function of a subnet mask?", "options": ["To divide an IP address into network and host portions", "To encrypt data packets", "To establish a VPN connection"], "answer": "To divide an IP address into network and host portions"},
        {"id": 11, "question": "Which command is used to test network connectivity in Windows?", "options": ["ping", "tracert", "ipconfig"], "answer": "ping"},
        {"id": 12, "question": "What is the purpose of the NAT protocol?", "options": ["To translate private IP addresses to public IP addresses", "To route packets between different networks", "To establish a secure connection"], "answer": "To translate private IP addresses to public IP addresses"},
        {"id": 13, "question": "Which of the following is a valid IPv6 address?", "options": ["2001:db8::ff00:42:8329", "192.168.1.1", "255.255.255.255"], "answer": "2001:db8::ff00:42:8329"},
        {"id": 14, "question": "What is the purpose of the SSL/TLS protocols?", "options": ["To secure communications over a computer network", "To assign IP addresses", "To route packets between networks"], "answer": "To secure communications over a computer network"},
        {"id": 15, "question": "Which of these is a valid way to configure a static IP address in Linux?", "options": ["/etc/network/interfaces", "/etc/sysconfig/network-scripts/ifcfg-eth0", "Both a and b"], "answer": "Both a and b"},
        {"id": 16, "question": "What is the function of a firewall in a network?", "options": ["To filter incoming and outgoing traffic", "To assign IP addresses", "To encrypt data"], "answer": "To filter incoming and outgoing traffic"},
        {"id": 17, "question": "Which protocol is used for secure data transmission over the internet?", "options": ["HTTP", "FTP", "HTTPS"], "answer": "HTTPS"},
        {"id": 18, "question": "What is the purpose of the ping command?", "options": ["To test network connectivity", "To display network configuration", "To trace the route to a network host"], "answer": "To test network connectivity"},
        {"id": 19, "question": "Which of the following is a network layer protocol?", "options": ["IP", "TCP", "UDP"], "answer": "IP"},
        {"id": 20, "question": "What is the function of the DNS protocol?", "options": ["To resolve domain names to IP addresses", "To route packets between networks", "To establish a secure connection"], "answer": "To resolve domain names to IP addresses"},
        {"id": 21, "question": "Which command is used to display the routing table in Linux?", "options": ["route", "netstat -r", "ip route"], "answer": "ip route"},
        {"id": 22, "question": "What is the purpose of the traceroute command?", "options": ["To trace the route packets take to a network host", "To display network configuration", "To test network connectivity"], "answer": "To trace the route packets take to a network host"},
        {"id": 23, "question": "Which of these is a valid way to configure a DHCP server in Linux?", "options": ["/etc/dhcp/dhcpd.conf", "/etc/sysconfig/dhcpd", "Both a and b"], "answer": "Both a and b"},
        {"id": 24, "question": "What is the function of the ARP protocol?", "options": ["To resolve IP addresses to MAC addresses", "To route packets between networks", "To establish a secure connection"], "answer": "To resolve IP addresses to MAC addresses"},
        {"id": 25, "question": "Which of the following is a valid way to display network configuration in Windows?", "options": ["ipconfig", "ifconfig", "netstat"], "answer": "ipconfig"},
        {"id": 26, "question": "What is the purpose of the netstat command?", "options": ["To display network connections, routing tables, and interface statistics", "To configure network interfaces", "To test network connectivity"], "answer": "To display network connections, routing tables, and interface statistics"},
        {"id": 27, "question": "Which protocol is used to securely connect to a remote server?", "options": ["SSH", "Telnet", "FTP"], "answer": "SSH"},
        {"id": 28, "question": "What is the function of a proxy server?", "options": ["To act as an intermediary between a client and a destination server", "To assign IP addresses", "To encrypt data"], "answer": "To act as an intermediary between a client and a destination server"},
        {"id": 29, "question": "Which of these is a valid way to configure a VPN in Linux?", "options": ["/etc/openvpn/client.conf", "/etc/ipsec.conf", "Both a and b"], "answer": "Both a and b"},
        {"id": 30, "question": "What is the purpose of the whois command?", "options": ["To display information about a domain name or IP address", "To test network connectivity", "To trace the route to a network host"], "answer": "To display information about a domain name or IP address"}
    ]
]

# Combine all questions
questions = python_questions + java_questions + c_questions + network_questions

# In-memory rooms and players
rooms = {}  # room_code: {"players": {username: {"answers": {}, "score": 0}}, "started": False, "topic": ..., "question_count": ..., "selected_questions": [...]}

def generate_room_code(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route("/")
def home():
    return "Quiz Backend is running with Flask 🚀"

# Create a new room
@app.route("/room", methods=["POST"])
def create_room():
    data = request.get_json(force=True)
    topic = data.get("topic", "python")
    question_count = int(data.get("question_count", 5))
    room_code = generate_room_code()
    # Filter questions by topic and randomly select
    filtered = [q for q in questions if q.get("topic") == topic]
    selected_questions = random.sample(filtered, min(question_count, len(filtered)))
    rooms[room_code] = {
        "players": {},
        "started": False,
        "topic": topic,
        "question_count": question_count,
        "selected_questions": selected_questions
    }
    return jsonify({"room_code": room_code})

# Join a room
@app.route("/room/<room_code>/join", methods=["POST"])
def join_room(room_code):
    data = request.json
    username = data.get("user")
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    if username in rooms[room_code]["players"]:
        return jsonify({"error": "User already in room"}), 400
    rooms[room_code]["players"][username] = {"answers": {}, "score": 0}
    return jsonify({"message": f"{username} joined room {room_code}"})

# Get quiz questions for a room (returns the random selection for this room)
@app.route("/room/<room_code>/quiz", methods=["GET"])
def get_room_quiz(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(rooms[room_code]["selected_questions"])

# Submit answers for a player in a room
@app.route("/room/<room_code>/submit", methods=["POST"])
def submit_room_answers(room_code):
    data = request.json
    username = data.get("user")
    answers = data.get("answers", {})
    if room_code not in rooms or username not in rooms[room_code]["players"]:
        return jsonify({"error": "Room or user not found"}), 404
    selected_questions = rooms[room_code]["selected_questions"]
    score = 0
    for q in selected_questions:
        qid = q["id"]
        if str(qid) in answers and answers[str(qid)] == q["answer"]:
            score += 1
    rooms[room_code]["players"][username]["answers"] = answers
    rooms[room_code]["players"][username]["score"] = score
    return jsonify({"user": username, "score": score, "total": len(selected_questions)})

# Get all players and their scores in a room
@app.route("/room/<room_code>/players", methods=["GET"])
def get_room_players(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    players = [
        {"user": user, "score": info["score"]}
        for user, info in rooms[room_code]["players"].items()
    ]
    return jsonify(players)

@app.route("/room/<room_code>/status", methods=["GET"])
def room_status(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    return jsonify({"started": rooms[room_code]["started"]})

@app.route("/room/<room_code>/start", methods=["POST"])
def start_quiz(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Room not found"}), 404
    rooms[room_code]["started"] = True
    return jsonify({"message": "Quiz started"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
