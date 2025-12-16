import { CloseToaster, SetMessage, ShowToaster } from "./Components/Toaster";
import { Toaster } from "./Components/Toaster";
import type { MessageTypeKey } from "./Components/Toaster";
import windowController from "./controllers/WindowController";
import type { WindowModelClass } from "./models/internal/windowModel";

function App() {

  let url = "http://localhost:5173"
  async function newWindow(){
    let wins = await windowController.get_all_windows() as WindowModelClass[]
    console.log(wins)
    windowController.add_window("test", url, wins[0].window_id)
  }

  return (
    <div className="main">
      hujniaasdawd
      <button onClick={() =>
        {
          SetMessage("WORKING" as MessageTypeKey, "This is a log message");
          ShowToaster();
          setTimeout(() => {
          SetMessage("LOG" as MessageTypeKey, "This is a log message");
          }, 1000);
          
        }
      }>show toster</button>

    <Toaster message="This is a toast message" />

    </div>

  );
}

export default App;