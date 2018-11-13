import sys.io.Process;
import haxe.io.Path;

class Main {

	function new() {
		var outputPath = 'output';
		var gpxPath = '../data/lon-vic/Track_2018-03-14 134847.gpx';
		var startTime_s = 6 * 60 + 38;
		var duration_s = 10;
		var saveGPXJson = true;

		// reset output
		if (sys.FileSystem.exists(outputPath)) {
			sys.FileSystem.deleteDirectory(outputPath);
		}
		sys.FileSystem.createDirectory(outputPath);

		var output = GPXParser.parse(gpxPath);

		if (saveGPXJson) {
			var jsonString = haxe.Json.stringify(output, null, '\t');
			sys.io.File.saveContent(Path.join([outputPath, 'gpx.json']), jsonString);
		}

		// find video file
		var videoPath = output.videoPath;
		if (!sys.FileSystem.exists(videoPath)) {
			videoPath = Path.join([Path.directory(gpxPath), Path.withoutDirectory(output.videoPath)]);
		}

		// get video framerate
		var result = js.node.ChildProcess.execSync('ffprobe -v 0 -of csv=p=0 -select_streams 0 -show_entries stream=r_frame_rate $videoPath');
		var fpsString = (result: js.node.Buffer).toString('utf8');
		var ab = fpsString.split('/');
		var fps = Std.parseFloat(ab[0])/Std.parseFloat(ab[1]);
		var frameTime_ms = 1000 / fps;

		trace('Frametime = $frameTime_ms ms');

		// var samplingDt_s = 0.250;
		var samplingFps = 4;
		var nSamples = Math.ceil(duration_s / 250);

		var endTime_s = startTime_s + duration_s;
		var startFrameIndex = Math.round((startTime_s * 1000) / frameTime_ms);
		var endFrameIndex = Math.round((endTime_s * 1000) / frameTime_ms);

		var imagePath = Path.join([outputPath, 'img%d.png']);
		var cmd = 'ffmpeg -i "$videoPath" -ss ${ffmpegSS(startTime_s)} -t ${ffmpegSS(duration_s)} -vf fps=$samplingFps -y "$imagePath"';

		var nFrames = duration_s * samplingFps;
		var gpsContinuum = new GPSContinuum(output.gpsReadings);

		for (i in 0...nFrames) {
			var frameTime_s = startTime_s + i * 1/samplingFps;

			// pick closest without interpolation
			var gps = gpsContinuum.get(frameTime_s);

			// add exif data
			var filePath = Path.join([outputPath, 'img$i.png']);

			metadata["Exif.GPSInfo.GPSLatitude"] = gps.latitude
			metadata["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
			metadata["Exif.GPSInfo.GPSLongitude"] = exiv_lon
			metadata["Exif.GPSInfo.GPSLongitudeRef"] = lon_deg[3]
			metadata["Exif.Image.GPSTag"] = 654
			metadata["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
			metadata["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'
			metadata["Exif.GPSInfo.GPSImgDirection"] = exiv_bearing
			metadata["Exif.GPSInfo.GPSImgDirectionRef"] = "T"
			if remove_image_description: metadata["Exif.Image.ImageDescription"] = []

			trace(i, frameTime_s, gps);
		}


		// Sys.command(cmd);

		// get GPS coordinates for each extracted frame

		//select=between(t\,10\,20)

		// get next frameNearest to frameNearest + nSamples

		/*
		for (gpsReading in output.gpsReadings) {
			if (gpsReading.time_s > (startTime_s + duration_s)) {
				break;
			}

			if (gpsReading.time_s >= startTime_s) {
				var frameFract = (gpsReading.time_s) * 1000 / frameTime_ms;

				var frameLow = Math.floor(frameFract);
				var frameHight = Math.ceil(frameFract);
				var frameNearest = Math.round(frameFract);

				// @! we can be up to 40ms off here, can maybe improve with some interpolation between gps readings
				var frameIndex = frameNearest;
				trace(frameIndex);

				var imagePath = Path.join([outputPath, 'frame-$frameIndex.png']);
				// trace('saving $imagePath');
				Sys.command('ffmpeg -i "$videoPath" -vf "select=gte(n\\,$frameIndex)" -vframes 1 "$imagePath" -y');
			}
		}
		*/


		// var exit = Sys.command('ffmpeg', []);
		// trace(exit);
		// var p = new Process('ffmpeg', [], false);
		// var exit = p.exitCode(true);
		// trace(p.stdout.readAll());
		// trace('err', p.stderr.readAll());
		// trace('exit', exit);
		// p.close();
	}

	function ffmpegSS(seconds) {
		var hours = Math.floor(seconds / 3600);
		var minutes = Math.floor((seconds - hours * 3600) / 60);
		var seconds = seconds - hours * 3600 - minutes * 60;

		return '${StringTools.lpad(Std.string(hours), '0', 2)}:${StringTools.lpad(Std.string(minutes), '0', 2)}:$seconds'; 
	}

	static function main() {
		new Main();
	}

}