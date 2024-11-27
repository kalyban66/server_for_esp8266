from flask import Flask, request, jsonify, Response
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Поріг для концентрації CO2
CO2_THRESHOLD = 1000  # ppm (parts per million)

@app.route('/soap', methods=['POST'])
def handle_soap():
    try:
        # Читання тіла запиту
        post_data = request.data

        # Парсинг SOAP-повідомлення
        root = ET.fromstring(post_data)
        body = root.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")
        if body is not None:
            co2_element = body.find("co2")
            if co2_element is not None and co2_element.text.isdigit():
                co2_level = int(co2_element.text)
                # Аналіз концентрації CO2
                if co2_level > CO2_THRESHOLD:
                    response_message = f"CO2 level is above the safe threshold: {co2_level} ppm."
                else:
                    response_message = f"CO2 level is within the safe range: {co2_level} ppm."
            else:
                response_message = "Invalid CO2 data provided."
        else:
            response_message = "Invalid SOAP message format."
    except ET.ParseError:
        response_message = "Failed to parse SOAP message."

    # Формування SOAP-відповіді
    response = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
       <soapenv:Body>
          <response>
             <text>{response_message}</text>
          </response>
       </soapenv:Body>
    </soapenv:Envelope>
    """
    return Response(response, content_type='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
