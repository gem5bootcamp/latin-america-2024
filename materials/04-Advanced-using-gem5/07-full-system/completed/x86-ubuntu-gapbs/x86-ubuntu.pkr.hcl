packer {
  required_plugins {
    qemu = {
      source  = "github.com/hashicorp/qemu"
      version = "~> 1"
    }
  }
}

variable "image_name" {
  type    = string
  default = "x86-ubuntu-24-04-gapbs"
}

variable "ssh_password" {
  type    = string
  default = "12345"
}

variable "ssh_username" {
  type    = string
  default = "gem5"
}

source "qemu" "initialize" {
  accelerator      = "kvm"
  boot_command     = ["<wait30>",
                      "gem5<enter><wait>",
                      "12345<enter><wait>",
                      "sudo mv /etc/netplan/50-cloud-init.yaml.bak /etc/netplan/50-cloud-init.yaml<enter><wait>",
                      "12345<enter><wait>",
                      "sudo netplan apply<enter><wait>",
                      "<wait>"]
  cpus             = "4"
  disk_size        = "5000"
  format           = "raw"
  headless         = "true"
  disk_image       = "true"
  iso_checksum     = "sha256:595e9b534c92d27f74082d31c95b3c7c0e2250d53e67c7391f810b0049fbc7a3"
  iso_urls         = ["/workspaces/2024/materials/02-Using-gem5/07-full-system/x86-ubuntu-generic/disk-image-ubuntu-24-04/x86-ubuntu-24-04"]
  memory           = "8192"
  output_directory = "disk-image-ubuntu-24-04"
  qemu_binary      = "/usr/bin/qemu-system-x86_64"
  qemuargs         = [["-cpu", "host"], ["-display", "none"]]
  shutdown_command = "echo '${var.ssh_password}'|sudo -S shutdown -P now"
  ssh_password     = "${var.ssh_password}"
  ssh_username     = "${var.ssh_username}"
  ssh_wait_timeout = "60m"
  vm_name          = "${var.image_name}"
  ssh_handshake_attempts = "1000"
}

build {
  sources = ["source.qemu.initialize"]

  provisioner "shell" {
    execute_command = "echo '${var.ssh_password}' | {{ .Vars }} sudo -E -S bash '{{ .Path }}'"
    scripts         = ["scripts/post-installation.sh"]
    expect_disconnect = true
  }

}
