import type Window from "../models/web_service/Window.tsx";


export class WindowController{

    windows: Window[] = []

    public add_window(window: Window){
        if(window !== undefined){
            this.windows.push(window);
        }
    }

    public delete_window(window_id: string){
        const found = this.windows.find(w => w.window.window_id === window_id) || undefined;
        if(found !== undefined){
            this.windows = this.windows.filter(w => w.window.window_id !== window_id);
        }
    }

    public get_window(window_id: string){
        return this.windows.find(w => w.window.window_id === window_id);
    }

    public get_all_windows(){
        return this.windows;
    }

}

