import axioClient from "../axioClient";

class HTTPController{
    

    //Windows API
    public create_window(title:string, url: string, parent_id: string) {
         axioClient.post('/window/create', {
            title: title,
            url: url,
            parent_id: parent_id
        }).then((response) => {
            if(response.data.error != undefined){
                console.error("Error creating window:", response.data.error.details);
                return response.data.error.status_code;
            }
            console.log("Window created:", response.data.success.message);
            return response.data.success.status_code;
        }).catch((error) => {
            console.error("Error creating window:", error);
            return 500;
        });
    }

    public get_window_by_id(window_id: string) {
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

    //Storage API
    public save_data_to_storage(window_id: string, key: string, value: string) {
        axioClient.post(`/window/${window_id}/storage`, {
            key: key,
            value: value
        }).then((response) => {
            if(response.data.error != undefined){
                console.error("Error saving data to storage:", response.data.error.details);
                return response.data.error.status_code;
            }
            console.log("Data saved to storage:", response.data.success.message);
            return response.data.success.status_code
        }).catch((error) => {
            console.error("Error saving data to storage:", error);
            return 500
        });
    }

    public get_data_from_storage(window_id: string, key: string) {
        return axioClient.get(`/window/${window_id}/storage/${key}`)
            .then((response) => {
                if(response.data.error != undefined){
                    console.error("Error fetching data from storage:", response.data.error.details);
                    return response.data.error.status_code;
                }
                return response.data.success.data.value;
            })
            .catch((error) => {500
                console.error("Error fetching data from storage:", error);
                return null
            });
    }

    public delete_data_from_storage(window_id: string, key: string){
        return axioClient.delete(`/window/${window_id}/storage/${key}`)
        .then((response) => {
            if(response.data.error != undefined){
                console.error(`Error deleting data from storage: ${response.data.error.details}`);
                return response.data.error.status_code;
            }
            console.log("Data successfully deleted from storage!");
            return response.data.success.status_code
        }).catch((error) => {
            console.error(`Error deleting data from storage: ${error}`);
            return 500
        })

    }
}