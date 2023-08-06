#include <string>
#include <arpa/inet.h>
#include <udt.h>
#include <boost/python.hpp>
#include <iostream>

class pyudt_socket {
  private:
  UDTSOCKET _sock;
  public:
  pyudt_socket() {
    _sock = UDT::socket(AF_INET, SOCK_DGRAM, 0);
    UDT::startup();
  };
  pyudt_socket(UDTSOCKET so): _sock(so) {
    UDT::startup();
  };
  ~pyudt_socket() {
    UDT::close(_sock);
  }

  bool bind(boost::python::tuple addr) {
    sockaddr_in my_addr;
    my_addr.sin_family = AF_INET;
    my_addr.sin_port = htons(boost::python::extract<int>(addr[1]));
    std::string ip = boost::python::extract<std::string>(addr[0]);
    inet_pton(AF_INET, ip.c_str(), &my_addr.sin_addr);
    memset(&(my_addr.sin_zero), '\0', 8);
    int r = UDT::bind(_sock,(sockaddr*)&my_addr,sizeof(my_addr));
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return false;
    }
    return true;
  }

  bool listen(int i) {
    int r = UDT::listen(_sock, i);
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return false;
    } 
    return true;
  }

  boost::python::tuple accept() {
    sockaddr_in addr;
    int namelen;
    UDTSOCKET recver = UDT::accept(_sock, (sockaddr*)&addr, &namelen);
    if (recver == UDT::INVALID_SOCK) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return boost::python::make_tuple();
    }
    pyudt_socket so(recver);
    std::string ip(inet_ntoa(addr.sin_addr));
    int port = ntohs(addr.sin_port);
    return boost::python::make_tuple(so, boost::python::make_tuple(ip, port));
  }

  std::string recv() {
    char buf[1024*1024];
    int r = UDT::recv(_sock, buf, 1024*1024, 0);
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return "";
    } else {
      return std::string(buf, r);
    }
  }

  int send(std::string data) {
    int r = UDT::send(_sock, data.c_str(), data.length(), 0);
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
    }
    return r;
  }

  bool connect(boost::python::tuple addr) {
    sockaddr_in peer;
    peer.sin_family = AF_INET;
    peer.sin_port = htons(boost::python::extract<int>(addr[1]));
    std::string ip = boost::python::extract<std::string>(addr[0]);
    inet_pton(AF_INET, ip.c_str(), &peer.sin_addr);
    memset(&(peer.sin_zero), '\0', 8);
    int r = UDT::connect(_sock, (sockaddr*)&peer, sizeof(peer));
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return false;
    }
    return true;
  }

  bool close() {
    int r = UDT::close(_sock);
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return false;
    }
    return true;
  }

  bool sendmsg(std::string msg) {
    int r = UDT::sendmsg(_sock, msg.c_str(), msg.length());
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return false;
    }
    return true;
  }

  std::string recvmsg() {
    char buf[1024*1024];
    int r = UDT::recvmsg(_sock, buf, 1024*1024);
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return "";
    }
    std::string data(buf, r);
    return data;
  }

  bool rendezvous() {
    bool flag = true;
    int r = UDT::setsockopt(_sock, 0, UDT_RENDEZVOUS, &flag, sizeof(bool));
    if (r == UDT::ERROR) {
      std::cerr << UDT::getlasterror().getErrorMessage() << std::endl;
      return false;
    }
    return true;
  }
};

BOOST_PYTHON_MODULE(pyudt) {
  using namespace boost::python;
  class_<pyudt_socket>("pyudt_socket")
    .def("bind", &pyudt_socket::bind)
    .def("listen", &pyudt_socket::listen)
    .def("accept", &pyudt_socket::accept)
    .def("recv", &pyudt_socket::recv)
    .def("send", &pyudt_socket::send)
    .def("connect", &pyudt_socket::connect)
    .def("close", &pyudt_socket::close)
    .def("sendmsg", &pyudt_socket::sendmsg)
    .def("recvmsg", &pyudt_socket::recvmsg)
    .def("rendezvous", &pyudt_socket::rendezvous)
  ;
};
