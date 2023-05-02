from flask import Flask, jsonify, request
from flasgger import Swagger
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import HttpResponseError
from azure.iot.deviceupdate import DeviceUpdateClient

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/update/list', methods=['GET'])
def list_updates():
    """
    Endpoint to list available device updates.
    ---
    parameters:
      - name: endpoint
        in: query
        type: string
        required: true
        description: The endpoint of the Device Update instance.
      - name: instance_id
        in: query
        type: string
        required: true
        description: The instance ID of the Device Update instance.
      - name: update_provider
        in: query
        type: string
        required: true
        description: The provider name of the device update.
      - name: update_name
        in: query
        type: string
        required: true
        description: The name of the device update.
      - name: update_version
        in: query
        type: string
        required: true
        description: The version of the device update.
    responses:
      200:
        description: A list of available device updates.
      400:
        description: One or more required parameters are missing.
      500:
        description: Failed to get data from the Device Update service.
    """
    try:
        endpoint = request.args.get('endpoint')
        instance_id = request.args.get('instance_id')
        update_provider = request.args.get('update_provider')
        update_name = request.args.get('update_name')
        Supdate_version = request.args.get('update_version')
    except KeyError:
        return jsonify({'message': 'Missing one or more required parameters'}), 400

    # Build a client through AAD
    client = DeviceUpdateClient(credential=DefaultAzureCredential(), endpoint=endpoint, instance_id=instance)

    try:
        response = {}

        # List providers
        providers = []
        provider_response = client.device_update.list_providers()
        for provider in provider_response:
            providers.append(provider)
        response['providers'] = providers

        # List names in provider
        names = []
        name_response = client.device_update.list_names(update_provider)
        for name in name_response:
            names.append(name)
        response['names'] = names

        # List versions in provider and name
        versions = []
        version_response = client.device_update.list_versions(update_provider, update_name)
        for version in version_response:
            versions.append(version)
        response['versions'] = versions

        return jsonify(response), 200
    except HttpResponseError as e:
        return jsonify({'message': 'Failed to get data', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
