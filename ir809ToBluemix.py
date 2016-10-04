import sys
import ibmiotf.api
import logging
import json

def main():
  try:
    with open('credentials.json') as data_file:    
      apiOptions  = json.load(data_file)
    
    logger = logging.getLogger("TestApi")
    apiClient   = ibmiotf.api.ApiClient(apiOptions, logger)

    deviceTypeId = "ir809"

    deviceId = "testDevice"
    authToken = "EcE592net"
    
    print("\nRegistering a new device") 
    print("Registered Device = ", apiClient.registerDevice(deviceTypeId, deviceId, authToken))
    
    print("\nRetrieving an existing device")  
    print(json.dumps(apiClient.getDevice(deviceTypeId, deviceId), indent=4, sort_keys=True))

    var = raw_input("Press Enter to stop")
    
    print("\nDeleting an existing device")
    deleted = apiClient.deleteDevice(deviceTypeId, deviceId)
    print("Device deleted = ", deleted)

  except ibmiotf.IoTFCReSTException as e:
    print(e.httpCode)
    print(str(e))
    sys.exit()



if __name__ == '__main__':
    main()