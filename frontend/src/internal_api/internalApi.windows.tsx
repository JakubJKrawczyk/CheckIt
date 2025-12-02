
import axioClient from "../axioClient.tsx";
import Windows_Storage from "./internalApi.windows.storage.tsx";

class Windows {

    storage: Windows_Storage = new Windows_Storage()


    //Windows API
    public async create_window(title:string, url: string, parent_id: string | undefined) {
         return axioClient.post('/window/create', {
            title: title,
            url: url,
            parent_id: parent_id
        }).then((response) => {
            if(response.data.error != undefined){
                console.error("Error creating window:", response.data.error.details);
                return response.data.error.status_code;
            }
            console.log("Window created:", response.data.success.message);
            return response.data.success.data["window_id"];
        }).catch((error) => {
            console.error("Error creating window:", error);
            return 500;
        });
    }

    public async get_window_by_id(window_id: string) {
        return axioClient.get(`/window/${window_id}`)
            .then((response) => {
                if(response.data.error != undefined){
                    console.error("Error fetching window:", response.data.error.details);
                    return null;
                }
                return response.data.success.data.window;
            })
            .catch((error) => {
                console.error("Error fetching window:", error);
                return null;
            });

    }

    public delete_window(window_id: string) {
        axioClient.delete(`/window/${window_id}`)
            .then((response) => {
                if(response.data.error != undefined){
                    console.error("Error deleting window:", response.data.error.details);
                    return response.data.error.status_code;
                }
                console.log("Window deleted:", response.data.success.message);
                return response.data.success.status_code;
            })
            .catch((error) => {
                console.error("Error deleting window:", error);
                return 500;
            });
    }

    public get_all_window() {
        return axioClient.get('/windows').then((response) => {
            if(response.data.error != undefined){
                console.error("Error fetching windows:", response.data.error.details);
                return null;
            }
            return response.data.success.data.windows;
        }).catch((error) => {
            console.error("Error fetching windows:", error);
            return null;
        });
    }
}

export default Windows