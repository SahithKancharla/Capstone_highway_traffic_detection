import {
    createBrowserRouter, 
    createRoutesFromElements, 
    Route 
  } from "react-router-dom";
  
  import PageLayout from "./components/PageLayout";
  
  import Home from "./pages/Home"
  import About from "./pages/About";
  import Map from "./pages/Map";
  
  const router = createBrowserRouter(
    createRoutesFromElements([
      // root pages:
      <Route path="/" element={<PageLayout />}>
        <Route index element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/map" element={<Map />}>
        </Route>
      </Route>,
  
      // full pages:
    ])
  );
  
  export default router;