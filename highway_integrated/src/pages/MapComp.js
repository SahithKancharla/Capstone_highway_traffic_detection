import React, { useState } from "react";
import {
    GoogleMap,
    withScriptjs,
    withGoogleMap,
    Marker,
    InfoWindow
} from "react-google-maps";
import properties from "./locations.json";

function MapComponent(){
    const [selectedProperty, setSelectedProperty] = useState(null);
    return (
        <GoogleMap
            defaultZoom={12}
            defaultCenter={{
                lat: 51.23651480350905,
                lng: -0.5703780104611352
            }}
        >
            {properties.map(property => (
                <Marker key = {property.id}
                position={{
                    lat: property.lat,
                    lng: property.lng
                }}
                icon={{
                    url: property.url,
                    scaledSize: new window.google.maps.Size(35,35),
                }}
                onClick = {() => {
                    setSelectedProperty(property);
                }}
                />
            ))}
            {selectedProperty && (
                <InfoWindow

                position = {{
                    lat:selectedProperty.lat,
                    lng:selectedProperty.lng
                }}
                onCloseClick= {() =>{
                    setSelectedProperty(null);
                }}
                >
                <div className = "try">
                <img className = "images" src= {require(`../${selectedProperty.img}`)}/>
                // this is the line that enable the communication between dynamic path and image rendering
                    <h4>{selectedProperty.name}</h4>
                </div>

                </InfoWindow>
            )}
        </GoogleMap>
    );
}

const WrappedMap = withScriptjs(withGoogleMap(MapComponent));

function MapComp(){
    return(
        <WrappedMap
        googleMapURL={`https://maps.googleapis.com/maps/api/js?key=AIzaSyDyACQK7rHe-82JIdvfex2jDQdTYdb6mos&callback=initMap`}
        loadingElement= {<div style={{height : "100%"}} />}
        containerElement = {<div style={{height : "100%"}} />}
        mapElement={<div style={{height : "100%"}} />}
        />
    )
}

export default MapComp;