import { Outlet } from "react-router-dom";

import Header from "./header";

function PageLayout() {
  return (
    <>
      <Header />
      
      <div className="page-content">
        <Outlet />
      </div>
      
    </>
  );
}

export default PageLayout;