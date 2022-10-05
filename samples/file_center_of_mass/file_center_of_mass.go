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

	fc, err := client.File.CreateCenterOfMass(
		densitySteelGramsPerCubicMillimeter,
		"obj",
		fileBytes,
	)
	if err != nil {
		panic(err)
	}
	fmt.Print(fc)
	fmt.Println("File center of mass: ", fc.CenterOfMass)

	json_data, _ := json.Marshal(struct {
		Title        string    `json:"title"`
		CenterOfMass []float64 `json:"center_of_mass"`
	}{
		Title:        "output.json",
		CenterOfMass: fc.CenterOfMass,
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
