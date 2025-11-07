resource "docker_network" "flamingo_net" {
  name = "flamingo_net"
}

output "network_name" {
  value = docker_network.flamingo_net.name
}
