<img src="https://raw.githubusercontent.com/wiki/yahanda/edge-realtime-object-detection/images/video-streaming-demo.gif" width="00">

# Installation

### Clone this repository
clone this repository by following command.
```
git clone git@github.com:yahanda/edge-realtime-object-detection.git
```

### Create an Azure Container Registry
1. Follow the instructions to [Quickstart: Create a private container registry using the Azure portal](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal)
1. After your container registry is created, browse to it, and from the left pane select **Access keys** from the menu located under **Settings**.
1. Enable Admin user and copy the values for **Login server**, **Username**, and **Password** and save them somewhere convenient.

### Build and Push IoT Edge Solution
1. Open git cloned folder with VS Code.
1. Update the `.env` with the values you made a note from Azure Container Registry.
1. Open the Visual Studio Code integrated terminal by selecting **View > Terminal**.
1. Sign in to Docker with the Azure container registry credentials that you saved after creating the registry.
    ```
    docker login -u <ACR username> -p <ACR password> <ACR login server>
    ```
1. Open the command palette and search for **Azure IoT Edge: Set Default Target Platform for Edge Solution**, or select the shortcut icon in the side bar at the bottom of the window.
1. In the command palette, select the target architecture from the list of options.
1. **Build and Push IoT Edge Solution** by right clicking on `deployment.template.json` file.


# The following sections are Under Construction...

### Run object detector on local windows machine
1. Pull the image from the Azure container registry
    ```
    docker pull <ACR login server>/objectdetector:0.0.1-amd64
    ```
1. Run the docker container
    ```
    docker run -t -i -p 8080:8080 <ACR login server>/objectdetector:0.0.1-amd64
    ```

### Run camera capture on local windows machine
1. Run the following command
    ```
    cd <cloned-folder>\edge-realtime-object-detection\modules\cameraCapture
    python main.py
    ```
1. Open the following URL in the browser
    ```
    http://localhost:5000
    ```
