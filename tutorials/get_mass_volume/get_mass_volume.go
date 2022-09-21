package main

import (
	"encoding/json"
	"fmt"
	"github.com/kittycad/kittycad.go"
	"os"
	"os/exec"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// KITTYCAD_API_TOKEN.
	client, _ := kittycad.NewClientFromEnv("your apps user agent")

	fileBytes, _ := os.ReadFile("./ORIGINALVOXEL-3.obj")
	// LITTERBOX-END-NON-EDITABLE-SECTION

	densitySteelGramsPerCubicMillimeter := 0.00784

	fc, _ := client.File.CreateMass(
		densitySteelGramsPerCubicMillimeter,
		"obj",
		fileBytes,
	)
	fv, _ := client.File.CreateVolume(
		"obj",
		fileBytes,
	)

	fmt.Println("File mass (g): ", fc.Mass)
	fmt.Println("File volume (mm^3): ", fv.Volume)

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
