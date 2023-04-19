import React from "react";
import "../styles/Map.css";
import MapComp from "./MapComp";

function Map(){
    return(
        <div id = "mapContainer">
            <div id = "mapClipPath">
                <MapComp/>
            </div>
        </div>
    )
}

export default Map;