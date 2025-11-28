
class WebsocketPayload{

    public type: string
    public target: string
    public payload: string

    constructor(type: string, target: string, payload: string = null) {
        this.type = type;
        this.target = target;
        this.payload = payload
    }
}

export default WebsocketPayload