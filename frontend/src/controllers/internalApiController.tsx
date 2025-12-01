import InternalApi from "../internal_api/InternalApi.tsx";


class InternalApiController{

    public api: InternalApi = new InternalApi()
   
}

const ApiController: InternalApiController = new InternalApiController()

export default ApiController