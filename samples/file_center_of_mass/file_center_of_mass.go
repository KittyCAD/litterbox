package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"github.com/kittycad/kittycad.go"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// ZOO_API_TOKEN.
	client, _ := kittycad.NewClientFromEnv("your apps user agent")

	fileBytes, _ := os.ReadFile("./seesaw.obj")
	// LITTERBOX-END-NON-EDITABLE-SECTION

	fc, err := client.File.CreateCenterOfMass(
		kittycad.UnitLengthMm,
		kittycad.FileImportFormatObj,
		fileBytes,
	)
	if err != nil {
		panic(err)
	}

	fmt.Println("File center of mass (mm): ", fc.CenterOfMass)

	json_data, _ := json.Marshal(struct {
		Title        string           `json:"title"`
		CenterOfMass kittycad.Point3D `json:"center_of_mass"`
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

	// Copy the original file to output.obj.
	if err := copyFile("./seesaw.obj", "./output.obj"); err != nil {
		panic(err)
	}

}

func copyFile(src, dst string) error {
	// Open the source file for reading
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	// Create the destination file
	dstFile, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer dstFile.Close()

	// Copy the content from src to dst
	_, err = io.Copy(dstFile, srcFile)
	if err != nil {
		return err
	}

	return nil
}
