typedef GPSReading = {
	time_s: Float,
	latitude: Float,
	longitude: Float,
	elevation: Float,
}

class GPXParser {
	
	static public function parse(path: String) {
		var gpsReadings = new Array<GPSReading>();

		var accelerationReadings = new Array<{
			time_s: Float,
			x: Float,
			y: Float,
			z: Float,
		}>();

		var content = sys.io.File.getContent(path);
		var xml = haxe.xml.Parser.parse(content, false);
		var f = new haxe.xml.Access(xml);
		var gpx = f.node.gpx;

		var metadata = gpx.node.metadata;		
		var time = metadata.node.time.innerData;
		// var timeUnix = js.Date.parse(time) / 100 0;

		var gpx = f.node.gpx;
		var trk = gpx.node.trk;
		var referenceFile = trk.node.link.att.href;
		var gpsStartOffset_s = Std.parseFloat(trk.node.extensions.node.resolve('gpxtrkoffx:TrackMovieOffsetExtension').node.resolve('gpxtrkoffx:StartOffsetSecs').innerData);

		var firstGPSNode = trk.node.trkseg.nodes.trkpt[0];
		var firstGPSTimeUnix = js.Date.parse(firstGPSNode.node.time.innerData) / 1000;
		var videoStartTimeUnix = firstGPSTimeUnix - gpsStartOffset_s;

		for (trkpt in trk.node.trkseg.nodes.trkpt) {
			var latitude = Std.parseFloat(trkpt.att.lat);
			var longitude = Std.parseFloat(trkpt.att.lon);
			var elevation = Std.parseFloat(trkpt.node.ele.innerData);
			var timeUnix = js.Date.parse(trkpt.node.time.innerData) / 1000;

			gpsReadings.push({
				time_s: timeUnix - videoStartTimeUnix,
				latitude: latitude,
				longitude: longitude,
				elevation: elevation,
			});

			var hasAcceleration = trkpt.hasNode.extensions && trkpt.node.extensions.hasNode.resolve('gpxacc:AccelerationExtension');
			var gpxaccNodes = hasAcceleration ? trkpt.node.extensions.node.resolve('gpxacc:AccelerationExtension').nodes.resolve('gpxacc:accel') : [];

			var acceleration = [
				for (gpxacc in gpxaccNodes) {
					offset_s: Std.parseFloat(gpxacc.att.offset) / 1000,
					x: Std.parseFloat(gpxacc.att.x),
					y: Std.parseFloat(gpxacc.att.y),
					z: Std.parseFloat(gpxacc.att.z),
				}
			];

			for (entry in acceleration) {
				accelerationReadings.push({
					time_s: timeUnix + entry.offset_s - videoStartTimeUnix,
					x: entry.x,
					y: entry.y,
					z: entry.z,
				});
			}
		}
		
		return {
			videoStartTimeUnix: videoStartTimeUnix,
			videoStartTimeIso: new js.Date(videoStartTimeUnix * 1000),
			videoPath: referenceFile,

			gpsReadings: gpsReadings,
			accelerationReadings: accelerationReadings
		}
	}

}