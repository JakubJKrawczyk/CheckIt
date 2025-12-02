import { WindowModelClass } from "../internal/windowModel.tsx"

class Window{

    /**
     *
     */
    constructor(w: WindowModelClass) {
        this.window = w
        this.websocket = undefined
    }

    public window: WindowModelClass
    public websocket: WebSocket | undefined
}

export default Window