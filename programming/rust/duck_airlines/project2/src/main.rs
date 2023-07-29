/**
 * The following uses the Haversine formula to compute the shortest distance
 * between two points (in this case, the LAT/LONG for the CLE and SLC airports)
 * on a sphere (in this case, the Earth).
 */
const EARTH_RADIUS_IN_KILOMETERS: f64 = 6371.0;

struct Waypoint {
    name: String,
    latitude: f64,
    longitude: f64,
}

fn make_waypoint(name: &str, latitude: f64, longitude: f64) -> Waypoint {
    return Waypoint{name: String::from(name), latitude: latitude,
        longitude: longitude};
}

fn distance_between_two_waypoints(previous_waypoint: &Waypoint, current_waypoint: &Waypoint) -> f64
{
    let previous_latitude_degrees: f64 = previous_waypoint.latitude;
    let previous_longitude_degrees: f64 = previous_waypoint.longitude;

    let current_latitude_degrees: f64 = current_waypoint.latitude;
    let current_longitude_degrees: f64 = current_waypoint.longitude;

    let previous_latitude_radians = previous_waypoint.latitude.to_radians();

    let current_latitude_radians = current_waypoint.latitude.to_radians();

    let delta_latitude = (previous_latitude_degrees - current_latitude_degrees).to_radians();
    let delta_longitude = (previous_longitude_degrees - current_longitude_degrees).to_radians();

    let inner_central_angle = f64::powi((delta_latitude / 2.0).sin(), 2)
        + previous_latitude_radians.cos()
        * current_latitude_radians.cos()
        * f64::powi((delta_longitude / 2.0).sin(), 2);
    let central_angle = 2.0 * inner_central_angle.sqrt().asin();

    let distance = EARTH_RADIUS_IN_KILOMETERS * central_angle;

    println!("The distance between {} and {} is {:.1} km.",
        previous_waypoint.name, current_waypoint.name, distance);

    return distance;
}

fn main() {

   let route: [Waypoint;21] = [
        make_waypoint("KCLE",  41.4075,  -81.851111),
        make_waypoint("LEYIR", 41.51030, -83.88080),
        make_waypoint("PIONS", 41.65390, -84.48190),
        make_waypoint("ZOSER", 41.72390, -84.78130),
        make_waypoint("MODEM", 41.72800, -84.89730),
        make_waypoint("BRYTO", 41.74170, -85.31320),
        make_waypoint("SEWTO", 41.74780, -85.51130),
        make_waypoint("GIJ",   41.76860, -86.31850),
        make_waypoint("NEPTS", 41.96750, -87.05300),
        make_waypoint("THORR", 42.12330, -87.60030),
        make_waypoint("OBK",   42.22140, -87.95160),
        make_waypoint("COTON", 42.31990, -89.31220),
        make_waypoint("DBQ",   42.40150, -90.70910),
        make_waypoint("VIGGR", 42.55520, -93.12410),
        make_waypoint("FOD",   42.51110, -94.29480),
        make_waypoint("ONL",   42.47050, -98.68690),
        make_waypoint("BFF",   41.89420, -103.48200),
        make_waypoint("OCS",   41.59020, -109.01500),
        make_waypoint("PUDVY", 41.54270, -109.34200),
        make_waypoint("WEGEM", 41.44560, -109.99000),
        make_waypoint("KSLC",  40.7861,  -111.9822)
    ];

    let mut total_distance: f64 = 0.0;
    let mut previous_waypoint: Option<&Waypoint> = None;

    for waypoint in route.iter() {
        match previous_waypoint {
            None => {
                previous_waypoint = Option::from(waypoint.clone());
                continue;
            },
            Some(..) => {
                let distance: f64 = distance_between_two_waypoints(
                    previous_waypoint.unwrap(), waypoint);
                total_distance += distance;
                previous_waypoint = Option::from(waypoint.clone());
            }
        }
    }

    println!("The total distance traveled over the course of the trip was: {:.1} km.",
        total_distance);
}
