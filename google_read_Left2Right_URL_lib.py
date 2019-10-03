

def google_vision_array_read_left_to_right(image):

    ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
    gkeypath = "AIzaSyAShkVK2p4rTM2XLhkcFJa7waOG0ALoRt4"
    api_key = gkeypath
    hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
            }

    img_requests = []
    try:
        _, encoded_image = cv2.imencode('.jpg', image)
        content = encoded_image.tobytes()
        ctxt = b64encode(content).decode()
        img_requests.append({
            'image': {'content': ctxt},
            'features': [{
                'type': 'TEXT_DETECTION'
            }]
        })

        img_encode = json.dumps({"requests": img_requests}).encode()
        req = urllib.request.Request(url=ENDPOINT_URL + api_key, headers=hdr)
        req.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(req, img_encode)
        abc = json.loads(response.read().decode("utf-8"))['responses']

        response2 = abc[0]['textAnnotations']
        items = []
        lines = {}

        for idx,text in enumerate(response2[1:]):
        #     print(text['description'])
            top_x_axis = response2[1:][idx]['boundingPoly']['vertices'][0]['x']

            top_y_axis = response2[1:][idx]['boundingPoly']['vertices'][0]['y']


            bottom_y_axis = response2[1:][idx]['boundingPoly']['vertices'][3]['y']

            if top_y_axis not in lines:
                lines[top_y_axis] = [(top_y_axis, bottom_y_axis), []]

            for s_top_y_axis, s_item in lines.items():
                if top_y_axis < s_item[0][1]:
                    lines[s_top_y_axis][1].append((top_x_axis, text['description']))
                    break

        for _, item in lines.items():
            if item[1]:
                words = sorted(item[1], key=lambda t: t[0])
                items.append((item[0], ' '.join([word for _, word in words]), words))

        text = ''
        for i in range(0,len(items)):
            a = items[i]
            text = text + ' ' + a[1]        
        
 
        return text

    except Exception as e:
        print('#2 Exception Occurred: {}'.format(e))
        # pass
        return ''
