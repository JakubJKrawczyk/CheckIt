import InternalApi from "../internal_api/internalApi.tsx";
import type { WindowModelClass } from "../models/internal/windowModel.tsx";

class WindowController{

    api: InternalApi = new InternalApi()

    // Backend is the source of truth - no local state!

    public async add_window(title: string, url: string, parent_id: string | undefined){
        return await this.api.windows.create_window(title, url, parent_id) as string
    }

    public async delete_window(window_id: string){
        await this.api.windows.delete_window(window_id)
    }

    public async get_window(window_id: string){
        return await this.api.windows.get_window_by_id(window_id) as WindowModelClass
    }

    public async get_all_windows(){
        return await this.api.windows.get_all_windows() as WindowModelClass[]
    }

}

const windowController: WindowController = new WindowController()

export default windowController
