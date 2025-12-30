import Windows from "./internalApi.windows"
import PdfApi from "./internalApi.pdf"

class InternalApi {

    public windows: Windows = new Windows()
    public pdf: PdfApi = new PdfApi()

}

export default InternalApi