import windowController from "./controllers/windowController";
import type { WindowModelClass } from "./models/internal/windowModel";

function App() {

  let url = "http://localhost:5173"
  async function newWindow(){
    let wins = await windowController.get_all_windows() as WindowModelClass[]
    console.log(wins)
    windowController.add_window("test", url, wins[0].window_id)
  }

  return (
    <div>
      hujniaasdawd
      <button onClick={newWindow}>New Window</button>
    </div>
  );
}

export default App;