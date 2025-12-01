
import axioClient from "../axioClient.tsx";

class Windows_Storage{

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
            .catch((error) => {
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

export default Windows_Storage