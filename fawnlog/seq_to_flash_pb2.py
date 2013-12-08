# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: seq_to_flash.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='seq_to_flash.proto',
  package='',
  serialized_pb='\n\x12seq_to_flash.proto\"S\n\x11SeqToFlashRequest\x12\x0f\n\x07\x64\x61ta_id\x18\x01 \x02(\x0c\x12\r\n\x05token\x18\x02 \x02(\x03\x12\x11\n\ttimestamp\x18\x03 \x02(\x02\x12\x0b\n\x03ips\x18\x04 \x02(\x02\"\x14\n\x12SeqToFlashResponse2E\n\x11SeqToFlashService\x12\x30\n\x05Write\x12\x12.SeqToFlashRequest\x1a\x13.SeqToFlashResponseB\x03\x90\x01\x01')




_SEQTOFLASHREQUEST = _descriptor.Descriptor(
  name='SeqToFlashRequest',
  full_name='SeqToFlashRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data_id', full_name='SeqToFlashRequest.data_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='token', full_name='SeqToFlashRequest.token', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='SeqToFlashRequest.timestamp', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ips', full_name='SeqToFlashRequest.ips', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=22,
  serialized_end=105,
)


_SEQTOFLASHRESPONSE = _descriptor.Descriptor(
  name='SeqToFlashResponse',
  full_name='SeqToFlashResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=107,
  serialized_end=127,
)

DESCRIPTOR.message_types_by_name['SeqToFlashRequest'] = _SEQTOFLASHREQUEST
DESCRIPTOR.message_types_by_name['SeqToFlashResponse'] = _SEQTOFLASHRESPONSE

class SeqToFlashRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SEQTOFLASHREQUEST

  # @@protoc_insertion_point(class_scope:SeqToFlashRequest)

class SeqToFlashResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SEQTOFLASHRESPONSE

  # @@protoc_insertion_point(class_scope:SeqToFlashResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')

_SEQTOFLASHSERVICE = _descriptor.ServiceDescriptor(
  name='SeqToFlashService',
  full_name='SeqToFlashService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=129,
  serialized_end=198,
  methods=[
  _descriptor.MethodDescriptor(
    name='Write',
    full_name='SeqToFlashService.Write',
    index=0,
    containing_service=None,
    input_type=_SEQTOFLASHREQUEST,
    output_type=_SEQTOFLASHRESPONSE,
    options=None,
  ),
])

class SeqToFlashService(_service.Service):
  __metaclass__ = service_reflection.GeneratedServiceType
  DESCRIPTOR = _SEQTOFLASHSERVICE
class SeqToFlashService_Stub(SeqToFlashService):
  __metaclass__ = service_reflection.GeneratedServiceStubType
  DESCRIPTOR = _SEQTOFLASHSERVICE

# @@protoc_insertion_point(module_scope)
