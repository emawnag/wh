# me - this DAT.
# webServerDAT - the connected Web Server DAT
# request - A dictionary of the request fields. The dictionary will always contain the below entries, plus any additional entries dependent on the contents of the request
# 		'method' - The HTTP method of the request (ie. 'GET', 'PUT').
# 		'uri' - The client's requested URI path. If there are parameters in the URI then they will be located under the 'pars' key in the request dictionary.
#		'pars' - The query parameters.
# 		'clientAddress' - The client's address.
# 		'serverAddress' - The server's address.
# 		'data' - The data of the HTTP request.
# response - A dictionary defining the response, to be filled in during the request method. Additional fields not specified below can be added (eg. response['content-type'] = 'application/json').
# 		'statusCode' - A valid HTTP status code integer (ie. 200, 401, 404). Default is 404.
# 		'statusReason' - The reason for the above status code being returned (ie. 'Not Found.').
# 		'data' - The data to send back to the client. If displaying a web-page, any HTML would be put here.

# Global variable for trigger state
var_trigger = False

# Global variables for additional state
x1, y1, x2, y2 = 0, 0, 0, 0
triggerMove = False
scale = 1.0  # New global variable for scale
sec = 0.0  # New global variable for sec
displayNone = False  # New global variable for displayNone

# return the response dictionary
def onHTTPRequest(webServerDAT, request, response):
    global var_trigger, x1, y1, x2, y2, triggerMove, scale, sec, displayNone
    
    # Set CORS headers
    response['Access-Control-Allow-Origin'] = '*'  # Allow all origins (change to specific domain if needed)
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    # Handle preflight request (CORS preflight request uses the OPTIONS method)
    if request['method'] == 'OPTIONS':
        response['statusCode'] = 200
        response['statusReason'] = 'OK'
        response['data'] = ''
        return response
    
    response['statusCode'] = 200 # OK
    response['statusReason'] = 'OK'
    
    # Route to set trigger to true
    if request['method'] == 'GET' and request['uri'] == '/trigger':
        var_trigger = True
        response['data'] = '{"trigger": true, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
        
    elif request['method'] == 'GET' and request['uri'] == '/UNtrigger':
        var_trigger = False
        response['data'] = '{"trigger": false, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
        
    # Route to get current trigger status
    elif request['method'] == 'GET' and request['uri'] == '/status':
        response['data'] = '{"trigger": %s, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (str(var_trigger).lower(), x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
    
    # Route to update coordinates
    elif request['method'] == 'GET' and request['uri'] == '/updateCoords':
        if 'x1' in request['pars']:
            x1 = int(request['pars']['x1'])
        if 'y1' in request['pars']:
            y1 = int(request['pars']['y1'])
        if 'x2' in request['pars']:
            x2 = int(request['pars']['x2'])
        if 'y2' in request['pars']:
            y2 = int(request['pars']['y2'])
        
        response['data'] = '{"trigger": %s, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (str(var_trigger).lower(), x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
    
    # Route to toggle triggerMove
    elif request['method'] == 'GET' and request['uri'] == '/toggleTriggerMove':
        triggerMove = not triggerMove
        response['data'] = '{"trigger": %s, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (str(var_trigger).lower(), x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
    
    # Route to toggle displayNone
    elif request['method'] == 'GET' and request['uri'] == '/toggleDisplayNone':
        displayNone = not displayNone
        response['data'] = '{"trigger": %s, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (str(var_trigger).lower(), x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
    
    # Route to update scale
    elif request['method'] == 'GET' and request['uri'] == '/updateScale':
        if 'scale' in request['pars']:
            scale = float(request['pars']['scale'])
        
        response['data'] = '{"trigger": %s, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (str(var_trigger).lower(), x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
    
    # Route to update sec
    elif request['method'] == 'GET' and request['uri'] == '/updateSec':
        if 'sec' in request['pars']:
            sec = float(request['pars']['sec'])
        
        response['data'] = '{"trigger": %s, "x1": %d, "y1": %d, "x2": %d, "y2": %d, "triggerMove": %s, "scale": %f, "sec": %f, "displayNone": %s}' % (str(var_trigger).lower(), x1, y1, x2, y2, str(triggerMove).lower(), scale, sec, str(displayNone).lower())
        response['content-type'] = 'application/json'
        return response
    
    # Default route
    else:
        response['data'] = '''
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .control-section { margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                .status-section { margin-top: 20px; }
                input[type="number"] { width: 60px; }
                button { margin: 5px; padding: 8px 12px; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1>TouchDesigner Control Panel: ''' + webServerDAT.name + '''</h1>
            
            <div class="control-section">
                <h2>Trigger Controls</h2>
                <button onclick="simulateAnchorClick(1)">Trigger Stone BOOM</button>
                <button onclick="simulateAnchorClick(0)">UNtrigger Stone BOOM</button>
            </div>
            
            <div class="control-section">
                <h2>Coordinate Controls</h2>
                <div>
                    <label>X1: <input type="number" id="x1Input" value="''' + str(x1) + '''"></label>
                    <label>Y1: <input type="number" id="y1Input" value="''' + str(y1) + '''"></label>
                    <label>X2: <input type="number" id="x2Input" value="''' + str(x2) + '''"></label>
                    <label>Y2: <input type="number" id="y2Input" value="''' + str(y2) + '''"></label>
                </div>
                <button onclick="updateCoordinates()">Update Coordinates</button>
            </div>
            
            <div class="control-section">
                <h2>TriggerMove Controls</h2>
                <button onclick="toggleTriggerMove()">Toggle TriggerMove</button>
                <span>Current state: <span id="triggerMoveStatus">''' + str(triggerMove).lower() + '''</span></span>
            </div>
            
            <div class="control-section">
                <h2>DisplayNone Controls</h2>
                <button onclick="toggleDisplayNone()">Toggle DisplayNone</button>
                <span>Current state: <span id="displayNoneStatus">''' + str(displayNone).lower() + '''</span></span>
            </div>
            
            <div class="control-section">
                <h2>Scale Control</h2>
                <div>
                    <label>Scale: <input type="number" id="scaleInput" value="''' + str(scale) + '''" step="0.1"></label>
                </div>
                <button onclick="updateScale()">Update Scale</button>
            </div>
            
            <div class="control-section">
                <h2>Sec Control</h2>
                <div>
                    <label>Sec: <input type="number" id="secInput" value="''' + str(sec) + '''" step="0.1"></label>
                </div>
                <button onclick="updateSec()">Update Sec</button>
            </div>
            
            <div class="status-section">
                <h2>Current Status</h2>
                <p>Trigger: <span id="triggerStatus">''' + str(var_trigger).lower() + '''</span></p>
                <p>X1: <span id="x1Status">''' + str(x1) + '''</span></p>
                <p>Y1: <span id="y1Status">''' + str(y1) + '''</span></p>
                <p>X2: <span id="x2Status">''' + str(x2) + '''</span></p>
                <p>Y2: <span id="y2Status">''' + str(y2) + '''</span></p>
                <p>Trigger Move: <span id="triggerMoveStatus2">''' + str(triggerMove).lower() + '''</span></p>
                <p>Display None: <span id="displayNoneStatus2">''' + str(displayNone).lower() + '''</span></p>
                <p>Scale: <span id="scaleStatus">''' + str(scale) + '''</span></p>
                <p>Sec: <span id="secStatus">''' + str(sec) + '''</span></p>
            </div>
            
            <script>
                function simulateAnchorClick(tf) {
                    const a = document.createElement("a");
                    a.href = tf ? "/trigger" : "/UNtrigger";
                    a.click();
                }
                
                function updateCoordinates() {
                    const x1 = document.getElementById('x1Input').value;
                    const y1 = document.getElementById('y1Input').value;
                    const x2 = document.getElementById('x2Input').value;
                    const y2 = document.getElementById('y2Input').value;
                    
                    fetch(`/updateCoords?x1=${x1}&y1=${y1}&x2=${x2}&y2=${y2}`)
                        .then(response => response.json())
                        .then(data => updateStatusDisplay(data));
                }
                
                function toggleTriggerMove() {
                    fetch('/toggleTriggerMove')
                        .then(response => response.json())
                        .then(data => updateStatusDisplay(data));
                }
                
                function toggleDisplayNone() {
                    fetch('/toggleDisplayNone')
                        .then(response => response.json())
                        .then(data => updateStatusDisplay(data));
                }
                
                function updateScale() {
                    const scale = document.getElementById('scaleInput').value;
                    fetch(`/updateScale?scale=${scale}`)
                        .then(response => response.json())
                        .then(data => updateStatusDisplay(data));
                }
                
                function updateSec() {
                    const sec = document.getElementById('secInput').value;
                    fetch(`/updateSec?sec=${sec}`)
                        .then(response => response.json())
                        .then(data => updateStatusDisplay(data));
                }
                
                function updateStatusDisplay(data) {
                    document.getElementById('triggerStatus').innerText = data.trigger;
                    document.getElementById('x1Status').innerText = data.x1;
                    document.getElementById('y1Status').innerText = data.y1;
                    document.getElementById('x2Status').innerText = data.x2;
                    document.getElementById('y2Status').innerText = data.y2;
                    document.getElementById('triggerMoveStatus').innerText = data.triggerMove;
                    document.getElementById('triggerMoveStatus2').innerText = data.triggerMove;
                    document.getElementById('displayNoneStatus').innerText = data.displayNone;
                    document.getElementById('displayNoneStatus2').innerText = data.displayNone;
                    document.getElementById('scaleStatus').innerText = data.scale;
                    document.getElementById('secStatus').innerText = data.sec;
                    
                    // Update input values
                    //document.getElementById('x1Input').value = data.x1;
                    //document.getElementById('y1Input').value = data.y1;
                    //document.getElementById('x2Input').value = data.x2;
                    //document.getElementById('y2Input').value = data.y2;
                    //document.getElementById('scaleInput').value = data.scale;
                    //document.getElementById('secInput').value = data.sec;
                }
                
                async function updateStatus() {
                    const response = await fetch('/status');
                    const data = await response.json();
                    updateStatusDisplay(data);
                }
                
                setInterval(updateStatus, 1000);
            </script>
        </body>
        </html>
        '''
        return response

def onWebSocketOpen(webServerDAT, client, uri):
    return

def onWebSocketClose(webServerDAT, client):
    return

def onWebSocketReceiveText(webServerDAT, client, data):
    webServerDAT.webSocketSendText(client, data)
    return

def onWebSocketReceiveBinary(webServerDAT, client, data):
    webServerDAT.webSocketSendBinary(client, data)
    return

def onWebSocketReceivePing(webServerDAT, client, data):
    webServerDAT.webSocketSendPong(client, data=data);
    return

def onWebSocketReceivePong(webServerDAT, client, data):
    return

def onServerStart(webServerDAT):
    global var_trigger, scale, sec, displayNone
    var_trigger = False  # Initialize trigger to False on server start
    scale = 1.0  # Initialize scale on server start
    sec = 0.0  # Initialize sec on server start
    displayNone = False  # Initialize displayNone on server start
    return

def onServerStop(webServerDAT):
    return