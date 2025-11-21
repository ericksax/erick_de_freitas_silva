package models

type Location struct {
	City      *string  `json:"city"`
	Latitude  float64  `json:"latitude"`
	Longitude float64  `json:"longitude"`
}

type WeatherPayload struct {
	Source                   string    `json:"source"`
	Location                 Location  `json:"location"`
	ObservedAt               string    `json:"observed_at"`
	TemperatureC             *float64  `json:"temperature_c"`
	HumidityPercent          *float64  `json:"humidity_percent"`
	WindSpeedMS              *float64  `json:"wind_speed_m_s"`
	WindDirectionDeg         *float64  `json:"wind_direction_deg"`
	CloudCoverPercent        *float64  `json:"cloud_cover_percent"`
	PrecipitationProbability *float64  `json:"precipitation_probability"`
	Raw                      any       `json:"raw"`
}
