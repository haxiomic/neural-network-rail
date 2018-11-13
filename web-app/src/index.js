import React from 'react'
import ReactDOM from 'react-dom'
import mapboxgl from 'mapbox-gl'
mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA';

require('./markers.css');

const markers = [
    {
        appear: (60 * 3 + 25) * 1000,
        location: (60 * 3 + 39) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 3 + 30) * 1000,
        location: (60 * 3 + 39) * 1000,
        image: require('./images/20.png'),
        rendered: false,
    },
    {
        appear: (60 * 4 + 22) * 1000,
        location: (60 * 4 + 33) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 4 + 45) * 1000,
        location: (60 * 4 + 55) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 5 + 3) * 1000,
        location: (60 * 5 + 5) * 1000,
        image: require('./images/35-60.png'),
        rendered: false,
    },
    {
        appear: (60 * 5 + 13) * 1000,
        location: (60 * 5 + 20) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 5 + 32) * 1000,
        location: (60 * 5 + 38) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 5 + 44) * 1000,
        location: (60 * 5 + 45) * 1000,
        image: require('./images/35-50.png'),
        rendered: false,
    },
    {
        appear: (60 * 5 + 45) * 1000,
        location: (60 * 5 + 45) * 1000,
        image: require('./images/35-50.png'),
        rendered: false,
    },
    {
        appear: (60 * 6 + 1) * 1000,
        location: (60 * 6 + 4) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 6 + 16) * 1000,
        location: (60 * 6 + 20) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 6 + 37) * 1000,
        location: (60 * 6 + 38) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 6 + 37) * 1000,
        location: (60 * 6 + 38) * 1000,
        image: require('./images/40-60.png'),
        rendered: false,
    },
    {
        appear: (60 * 6 + 46) * 1000,
        location: (60 * 6 + 51) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 7 + 3) * 1000,
        location: (60 * 7 + 9) * 1000,
        image: require('./images/signal.png'),
        rendered: false,
    },
    {
        appear: (60 * 7 + 16) * 1000,
        location: (60 * 7 + 18) * 1000,
        image: require('./images/40-50.png'),
        rendered: false,
    },
    {
        appear: (60 * 7 + 16) * 1000,
        location: (60 * 7 + 18) * 1000,
        image: require('./images/40-60.png'),
        rendered: false,
    },
    {
        appear: (60 * 7 + 23) * 1000,
        location: (60 * 7 + 24) * 1000,
        image: require('./images/40-60.png'),
        rendered: false,
    },
    {
        appear: (60 * 7 + 24) * 1000,
        location: (60 * 7 + 25) * 1000,
        image: require('./images/25.png'),
        rendered: false,
    }
]

const loadGeoJson = async (endpoint) => {
    const response = await fetch(endpoint)
    const json = await response.json();
    return json;
}

const stripPoints = (geoJson) => {
    const coordTimes = geoJson.features[0].properties.coordTimes
    const coordinates = geoJson.features[0].geometry.coordinates
    const length = Math.max(coordinates.length, coordTimes.length)
    return { coordinates, coordTimes, length }
}

const createBaseGeoJson = () => ({
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "2018-03-14 13:48:47",
                "time": "2018-03-14T12:48:48Z",
                "coordTimes": [],
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [],
            }
        }
    ]
})

const sleep = (duration) => new Promise((resolve) => setTimeout(resolve, duration));

const dateValue = (string = '') => (string.length) ? (new Date(string)).valueOf() : Date.now();

const originalBase = createBaseGeoJson();

class Application extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            coords: 0,
            lng: -0.0714,
            lat: 51.4555,
            zoom: 12,
        };
    }

    componentDidMount() {
        const { lng, lat, zoom } = this.state;

        const map = new mapboxgl.Map({
            container: this.mapContainer,
            style: 'mapbox://styles/mapbox/streets-v9',
            center: [lng, lat],
            zoom
        });

        const createMarker = (coordinates, image) => {
            // create a HTML element for each feature
            const element = document.createElement('div');
            element.className = 'marker';
            element.style['background-image'] = `url(${image})`;
            // make a marker for each feature and add to the map
            const marker = new mapboxgl.Marker(element)
            marker.setLngLat({
                lng: coordinates[0],
                lat: coordinates[1],
            }).addTo(map);
        }

        map.on('load', async () => {

            let i = 0;
            const next = () => i += 1;
            const timeZero = dateValue();

            const full = await loadGeoJson(require('./original.geojson'));
            const { coordinates, coordTimes, length } = stripPoints(full);

            const firstCoordTime = dateValue(coordTimes[0]);
            const targetStartTime = firstCoordTime + (60 * 3 + 20) * 1000; // Start 4 minutes into route
            const realTimeOffset = timeZero - targetStartTime; // Will be positive
            // Add all existing route to map before render
            while (dateValue(coordTimes[i]) < (dateValue() - realTimeOffset)) {
                let coordTime = coordTimes[i]
                let coordinate = coordinates[i]
                originalBase.features[0].properties.coordTimes.push(coordTime)
                originalBase.features[0].geometry.coordinates.push(coordinate)
                next()
            }

            map.addLayer({
                'id': 'line-animation',
                'type': 'line',
                'source': {
                    'type': 'geojson',
                    'data': originalBase,
                },
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#ed6498',
                    'line-width': 5,
                    'line-opacity': .8
                }
            });

            const animate = async () => {
                let coordTime = coordTimes[i]
                if (dateValue(coordTime) < (dateValue() - realTimeOffset)) {
                    let coordinate = coordinates[i]
                    originalBase.features[0].properties.coordTimes.push(coordTime)
                    originalBase.features[0].geometry.coordinates.push(coordinate)
                    map.getSource('line-animation').setData(originalBase);
                    map.flyTo({ center: coordinate.slice(0, 2), zoom: 17, });
                    next();
                }
                const routeRuntime = dateValue(coordTime) - firstCoordTime;
                markers.filter(({ rendered }) => !rendered).forEach((marker) => {
                    const { appear, location, image } = marker
                    if (appear < routeRuntime) {
                        const index = coordTimes.slice(i).findIndex((coordTime) => {
                            const routeRuntime = dateValue(coordTime) - firstCoordTime;
                            return (location < routeRuntime)
                        })
                        createMarker(coordinates[index + i], image);
                        marker.rendered = true;
                    }
                })
                if (i < length) {
                    await sleep(100);
                    requestAnimationFrame(animate);
                }
            }
            animate();
        })

    }

    render() {
        const { lng, lat, zoom } = this.state;

        return (
            <div>
                <div className="inline-block absolute top left mt12 ml12 bg-darken75 color-white z1 py6 px12 round-full txt-s txt-bold">
                    <div>{`Longitude: ${lng} Latitude: ${lat} Zoom: ${zoom}`}</div>
                </div>
                <div ref={el => this.mapContainer = el} className="absolute top right left bottom" />
            </div>
        );
    }
}

ReactDOM.render(<Application />, document.getElementById('app'));
