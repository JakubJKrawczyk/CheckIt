
import windowController from "../src/controllers/windowController.tsx"
 
async function  App() {

  await windowController.add_window("test", "http://localhost:3000", undefined)

  return (
    <div>
      hujniaasdawd
    </div>
  );
}

export default App;