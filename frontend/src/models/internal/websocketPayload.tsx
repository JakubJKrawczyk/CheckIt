
class WebsocketPayload{

    public type: string
    public target: string
    public payload: string | undefined

    constructor(type: string, target: string, payload: string | undefined = undefined) {
        this.type = type;
        this.target = target;
        this.payload = payload
    }
}

export default WebsocketPayload