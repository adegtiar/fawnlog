# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flash_service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import service as _service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='flash_service.proto',
  package='',
  serialized_pb='\n\x13\x66lash_service.proto\"\x1d\n\x0bReadRequest\x12\x0e\n\x06offset\x18\x01 \x02(\x03\"\x85\x01\n\x0cReadResponse\x12$\n\x06status\x18\x01 \x02(\x0e\x32\x14.ReadResponse.Status\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"A\n\x06Status\x12\x0b\n\x07SUCCESS\x10\x00\x12\x13\n\x0f\x45RROR_UNWRITTEN\x10\x01\x12\x15\n\x11\x45RROR_FILLED_HOLE\x10\x02\"-\n\x0cWriteRequest\x12\x0f\n\x07\x64\x61ta_id\x18\x01 \x02(\x0c\x12\x0c\n\x04\x64\x61ta\x18\x02 \x02(\x0c\"\\\n\nIpsMeasure\x12\r\n\x05token\x18\x01 \x02(\x03\x12\x19\n\x11request_timestamp\x18\x02 \x02(\x03\x12\x17\n\x0ftoken_timestamp\x18\x03 \x02(\x03\x12\x0b\n\x03ips\x18\x04 \x02(\x02\"\xca\x01\n\rWriteResponse\x12%\n\x06status\x18\x01 \x02(\x0e\x32\x15.WriteResponse.Status\x12\x1c\n\x07measure\x18\x02 \x01(\x0b\x32\x0b.IpsMeasure\"t\n\x06Status\x12\x0b\n\x07SUCCESS\x10\x00\x12\x15\n\x11\x45RROR_OVERWRITTEN\x10\x01\x12\x15\n\x11\x45RROR_FILLED_HOLE\x10\x02\x12\x18\n\x14\x45RROR_OVERSIZED_DATA\x10\x03\x12\x15\n\x11\x45RROR_NO_CAPACITY\x10\x04\"!\n\x0f\x46illHoleRequest\x12\x0e\n\x06offset\x18\x01 \x02(\x03\"j\n\x10\x46illHoleResponse\x12(\n\x06status\x18\x01 \x02(\x0e\x32\x18.FillHoleResponse.Status\",\n\x06Status\x12\x0b\n\x07SUCCESS\x10\x00\x12\x15\n\x11\x45RROR_OVERWRITTEN\x10\x01\"\x0e\n\x0cResetRequest\"X\n\rResetResponse\x12%\n\x06status\x18\x01 \x02(\x0e\x32\x15.ResetResponse.Status\" \n\x06Status\x12\x0b\n\x07SUCCESS\x10\x00\x12\t\n\x05\x45RROR\x10\x01\"d\n\x12WriteOffsetRequest\x12\x0f\n\x07\x64\x61ta_id\x18\x01 \x02(\x0c\x12\x0e\n\x06offset\x18\x02 \x02(\x03\x12\x0f\n\x07is_full\x18\x03 \x02(\x08\x12\x1c\n\x07measure\x18\x04 \x02(\x0b\x32\x0b.IpsMeasure\"\x15\n\x13WriteOffsetResponse2\xee\x01\n\x0c\x46lashService\x12#\n\x04Read\x12\x0c.ReadRequest\x1a\r.ReadResponse\x12&\n\x05Write\x12\r.WriteRequest\x1a\x0e.WriteResponse\x12/\n\x08\x46illHole\x12\x10.FillHoleRequest\x1a\x11.FillHoleResponse\x12&\n\x05Reset\x12\r.ResetRequest\x1a\x0e.ResetResponse\x12\x38\n\x0bWriteOffset\x12\x13.WriteOffsetRequest\x1a\x14.WriteOffsetResponseB\x03\x90\x01\x01')



_READRESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='ReadResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_UNWRITTEN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_FILLED_HOLE', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=123,
  serialized_end=188,
)

_WRITERESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='WriteResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_OVERWRITTEN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_FILLED_HOLE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_OVERSIZED_DATA', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_NO_CAPACITY', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=418,
  serialized_end=534,
)

_FILLHOLERESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='FillHoleResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_OVERWRITTEN', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=418,
  serialized_end=462,
)

_RESETRESPONSE_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='ResetResponse.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=751,
  serialized_end=783,
)


_READREQUEST = _descriptor.Descriptor(
  name='ReadRequest',
  full_name='ReadRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='offset', full_name='ReadRequest.offset', index=0,
      number=1, type=3, cpp_type=2, label=2,
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
  serialized_start=23,
  serialized_end=52,
)


_READRESPONSE = _descriptor.Descriptor(
  name='ReadResponse',
  full_name='ReadResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='ReadResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='ReadResponse.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _READRESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=55,
  serialized_end=188,
)


_WRITEREQUEST = _descriptor.Descriptor(
  name='WriteRequest',
  full_name='WriteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data_id', full_name='WriteRequest.data_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='WriteRequest.data', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
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
  serialized_start=190,
  serialized_end=235,
)


_IPSMEASURE = _descriptor.Descriptor(
  name='IpsMeasure',
  full_name='IpsMeasure',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='IpsMeasure.token', index=0,
      number=1, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request_timestamp', full_name='IpsMeasure.request_timestamp', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='token_timestamp', full_name='IpsMeasure.token_timestamp', index=2,
      number=3, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ips', full_name='IpsMeasure.ips', index=3,
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
  serialized_start=237,
  serialized_end=329,
)


_WRITERESPONSE = _descriptor.Descriptor(
  name='WriteResponse',
  full_name='WriteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='WriteResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='measure', full_name='WriteResponse.measure', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _WRITERESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=332,
  serialized_end=534,
)


_FILLHOLEREQUEST = _descriptor.Descriptor(
  name='FillHoleRequest',
  full_name='FillHoleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='offset', full_name='FillHoleRequest.offset', index=0,
      number=1, type=3, cpp_type=2, label=2,
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
  serialized_start=536,
  serialized_end=569,
)


_FILLHOLERESPONSE = _descriptor.Descriptor(
  name='FillHoleResponse',
  full_name='FillHoleResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='FillHoleResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _FILLHOLERESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=571,
  serialized_end=677,
)


_RESETREQUEST = _descriptor.Descriptor(
  name='ResetRequest',
  full_name='ResetRequest',
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
  serialized_start=679,
  serialized_end=693,
)


_RESETRESPONSE = _descriptor.Descriptor(
  name='ResetResponse',
  full_name='ResetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='ResetResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RESETRESPONSE_STATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=695,
  serialized_end=783,
)


_WRITEOFFSETREQUEST = _descriptor.Descriptor(
  name='WriteOffsetRequest',
  full_name='WriteOffsetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data_id', full_name='WriteOffsetRequest.data_id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='offset', full_name='WriteOffsetRequest.offset', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_full', full_name='WriteOffsetRequest.is_full', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='measure', full_name='WriteOffsetRequest.measure', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=785,
  serialized_end=885,
)


_WRITEOFFSETRESPONSE = _descriptor.Descriptor(
  name='WriteOffsetResponse',
  full_name='WriteOffsetResponse',
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
  serialized_start=887,
  serialized_end=908,
)

_READRESPONSE.fields_by_name['status'].enum_type = _READRESPONSE_STATUS
_READRESPONSE_STATUS.containing_type = _READRESPONSE;
_WRITERESPONSE.fields_by_name['status'].enum_type = _WRITERESPONSE_STATUS
_WRITERESPONSE.fields_by_name['measure'].message_type = _IPSMEASURE
_WRITERESPONSE_STATUS.containing_type = _WRITERESPONSE;
_FILLHOLERESPONSE.fields_by_name['status'].enum_type = _FILLHOLERESPONSE_STATUS
_FILLHOLERESPONSE_STATUS.containing_type = _FILLHOLERESPONSE;
_RESETRESPONSE.fields_by_name['status'].enum_type = _RESETRESPONSE_STATUS
_RESETRESPONSE_STATUS.containing_type = _RESETRESPONSE;
_WRITEOFFSETREQUEST.fields_by_name['measure'].message_type = _IPSMEASURE
DESCRIPTOR.message_types_by_name['ReadRequest'] = _READREQUEST
DESCRIPTOR.message_types_by_name['ReadResponse'] = _READRESPONSE
DESCRIPTOR.message_types_by_name['WriteRequest'] = _WRITEREQUEST
DESCRIPTOR.message_types_by_name['IpsMeasure'] = _IPSMEASURE
DESCRIPTOR.message_types_by_name['WriteResponse'] = _WRITERESPONSE
DESCRIPTOR.message_types_by_name['FillHoleRequest'] = _FILLHOLEREQUEST
DESCRIPTOR.message_types_by_name['FillHoleResponse'] = _FILLHOLERESPONSE
DESCRIPTOR.message_types_by_name['ResetRequest'] = _RESETREQUEST
DESCRIPTOR.message_types_by_name['ResetResponse'] = _RESETRESPONSE
DESCRIPTOR.message_types_by_name['WriteOffsetRequest'] = _WRITEOFFSETREQUEST
DESCRIPTOR.message_types_by_name['WriteOffsetResponse'] = _WRITEOFFSETRESPONSE

class ReadRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _READREQUEST

  # @@protoc_insertion_point(class_scope:ReadRequest)

class ReadResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _READRESPONSE

  # @@protoc_insertion_point(class_scope:ReadResponse)

class WriteRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _WRITEREQUEST

  # @@protoc_insertion_point(class_scope:WriteRequest)

class IpsMeasure(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _IPSMEASURE

  # @@protoc_insertion_point(class_scope:IpsMeasure)

class WriteResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _WRITERESPONSE

  # @@protoc_insertion_point(class_scope:WriteResponse)

class FillHoleRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FILLHOLEREQUEST

  # @@protoc_insertion_point(class_scope:FillHoleRequest)

class FillHoleResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FILLHOLERESPONSE

  # @@protoc_insertion_point(class_scope:FillHoleResponse)

class ResetRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESETREQUEST

  # @@protoc_insertion_point(class_scope:ResetRequest)

class ResetResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESETRESPONSE

  # @@protoc_insertion_point(class_scope:ResetResponse)

class WriteOffsetRequest(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _WRITEOFFSETREQUEST

  # @@protoc_insertion_point(class_scope:WriteOffsetRequest)

class WriteOffsetResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _WRITEOFFSETRESPONSE

  # @@protoc_insertion_point(class_scope:WriteOffsetResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\220\001\001')

_FLASHSERVICE = _descriptor.ServiceDescriptor(
  name='FlashService',
  full_name='FlashService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=911,
  serialized_end=1149,
  methods=[
  _descriptor.MethodDescriptor(
    name='Read',
    full_name='FlashService.Read',
    index=0,
    containing_service=None,
    input_type=_READREQUEST,
    output_type=_READRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Write',
    full_name='FlashService.Write',
    index=1,
    containing_service=None,
    input_type=_WRITEREQUEST,
    output_type=_WRITERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='FillHole',
    full_name='FlashService.FillHole',
    index=2,
    containing_service=None,
    input_type=_FILLHOLEREQUEST,
    output_type=_FILLHOLERESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Reset',
    full_name='FlashService.Reset',
    index=3,
    containing_service=None,
    input_type=_RESETREQUEST,
    output_type=_RESETRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='WriteOffset',
    full_name='FlashService.WriteOffset',
    index=4,
    containing_service=None,
    input_type=_WRITEOFFSETREQUEST,
    output_type=_WRITEOFFSETRESPONSE,
    options=None,
  ),
])

class FlashService(_service.Service):
  __metaclass__ = service_reflection.GeneratedServiceType
  DESCRIPTOR = _FLASHSERVICE
class FlashService_Stub(FlashService):
  __metaclass__ = service_reflection.GeneratedServiceStubType
  DESCRIPTOR = _FLASHSERVICE

# @@protoc_insertion_point(module_scope)
