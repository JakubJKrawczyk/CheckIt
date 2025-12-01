import {WindowController} from "./controllers/WindowController.tsx";
import ApiController from "./controllers/InternalApiController.tsx";

async function  App() {

  const controller: WindowController = new WindowController()

  const w: string = await ApiController.api.windows.create_window("test", "http://localhost:3000", undefined)
  let win = await ApiController.api.windows.get_window_by_id(w)
  controller.add_window(win)

  return (
    <div>
      hujniaasdawd
    </div>
  );
}

export default App;