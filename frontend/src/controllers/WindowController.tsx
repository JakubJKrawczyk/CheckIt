import InternalApi from "../internal_api/internalApi.tsx";
import { WindowModelClass } from "../models/internal/windowModel.tsx";
import Window from "../models/web_service/Window.tsx";


class WindowController{

    api: InternalApi = new InternalApi()
    windows: Window[] = []

    public async add_window(title:string, url: string, parent_id: string | undefined){

        let w_id = await this.api.windows.create_window(title, url, parent_id)
        let w_internal = await this.api.windows.get_window_by_id(w_id)
        let w_object = new Window(w_internal)

            this.windows.push(w_object);
    }

    public delete_window(window_id: string){
        const found = this.windows.find(w => w.window.window_id === window_id) || undefined;
        if(found !== undefined){
            this.windows = this.windows.filter(w => w.window.window_id !== window_id);
        }
    }

    public async sync_windows(){
        let windows_backend : WindowModelClass[] = await this.api.windows.get_all_window()

        windows_backend.forEach(w => {
            if(this.windows.find(ww => ww.window.window_id == w.window_id) == undefined){
                this.windows.push(new Window(w))
            }
        });

        this.windows.forEach(w => {
            let wb = windows_backend.find(wb => wb.window_id == w.window.window_id)
            if(wb == undefined){
               this.delete_window(w.window.window_id as string)
            }
        })
    }

    public get_window(window_id: string){
        return this.windows.find(w => w.window.window_id === window_id);
    }

    public get_all_windows(){
        return this.windows;
    }

}

const windowController: WindowController = new WindowController()

export default windowController

