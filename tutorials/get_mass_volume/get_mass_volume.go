package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"

	"github.com/kittycad/kittycad.go"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// KITTYCAD_API_TOKEN.
	client, _ := kittycad.NewClientFromEnv("your apps user agent")

	fileBytes, _ := os.ReadFile("./ORIGINALVOXEL-3.obj")
	// LITTERBOX-END-NON-EDITABLE-SECTION

	// We divide by 1e+9 here to convert from cubic millimeters to cubic meters.
	densitySteelGramsPerCubicMeter := 0.00784 / 1e+9

	fc, _ := client.File.CreateMass(
		densitySteelGramsPerCubicMeter,
		kittycad.UnitDensityKgm3,
		kittycad.UnitMasG,
		kittycad.FileImportFormatObj,
		fileBytes,
	)
	fv, _ := client.File.CreateVolume(
		kittycad.UnitVolumeM3,
		kittycad.FileImportFormatObj,
		fileBytes,
	)

	fmt.Println("File mass (g): ", fc.Mass)
	fmt.Println("File volume (m^3): ", fv.Volume)

	json_data, _ := json.Marshal(struct {
		Title  string  `json:"title"`
		Mass   float64 `json:"mass"`
		Volume float64 `json:"volume"`
	}{
		Title:  "output.json",
		Mass:   fc.Mass,
		Volume: fv.Volume,
	})

	// LITTERBOX-START-NON-EDITABLE-SECTION
	output_file_path := "./output.json"
	output, _ := os.Create(output_file_path)
	defer output.Close()
	output.Write(json_data)
	if err := output.Sync(); err != nil {
		panic(err)
	}
	exec.Command("cp", "./ORIGINALVOXEL-3.obj", "./output.obj").Output()
}
