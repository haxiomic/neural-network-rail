const fs = require('fs-extra');
const { DOMParser } = require('xmldom');
const togeojson = require('@mapbox/togeojson');

console.log(togeojson)

const parseFile = async (name) => {
    const strong = await fs.readFile(`./data/${name}.gpx`, 'utf8');
    const gpx = new DOMParser().parseFromString(strong);
    const converted = togeojson.gpx(gpx, { styles: true });
    await fs.writeJson(`./public/${name}.geojson`, converted, { spaces: 4 });
}

const promise = parseFile('original')
promise.then(() => console.log('compete'))
promise.catch((error) => console.log(error))