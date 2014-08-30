# encoding: utf-8

"""
Test suite for pptx.chart.xlsx module
"""

from __future__ import absolute_import, print_function

import pytest

from StringIO import StringIO as BytesIO

from xlsxwriter.worksheet import Worksheet

from pptx.chart.xlsx import WorkbookWriter

from ..unitutil.mock import class_mock, instance_mock, method_mock


class Describe_WorkbookWriter(object):

    def it_can_generate_a_chart_data_Excel_blob(self, xlsx_blob_fixture):
        categories_, series_, xlsx_file_ = xlsx_blob_fixture[:3]
        _populate_worksheet_, worksheet_, xlsx_blob_ = xlsx_blob_fixture[3:]

        xlsx_blob = WorkbookWriter.xlsx_blob(categories_, series_)

        WorkbookWriter._open_worksheet.assert_called_once_with(xlsx_file_)
        _populate_worksheet_.assert_called_once_with(
            worksheet_, categories_, series_
        )
        assert xlsx_blob is xlsx_blob_

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def xlsx_blob_fixture(
            self, request, categories, series_lst_, xlsx_file_, BytesIO_,
            _open_worksheet_, worksheet_, _populate_worksheet_, xlsx_blob_):
        return (
            categories, series_lst_, xlsx_file_, _populate_worksheet_,
            worksheet_, xlsx_blob_
        )

    # fixture components ---------------------------------------------

    @pytest.fixture
    def BytesIO_(self, request, xlsx_file_):
        return class_mock(
            request, 'pptx.chart.xlsx.BytesIO', return_value=xlsx_file_
        )

    @pytest.fixture
    def categories(self):
        return ('Foo', 'Bar')

    @pytest.fixture
    def _open_worksheet_(self, request, worksheet_):
        open_worksheet_ = method_mock(
            request, WorkbookWriter, '_open_worksheet'
        )
        # to make context manager behavior work
        open_worksheet_.return_value.__enter__.return_value = worksheet_
        return open_worksheet_

    @pytest.fixture
    def _populate_worksheet_(self, request):
        return method_mock(request, WorkbookWriter, '_populate_worksheet')

    @pytest.fixture
    def series_lst_(self, request):
        return instance_mock(request, list)

    @pytest.fixture
    def worksheet_(self, request):
        return instance_mock(request, Worksheet)

    @pytest.fixture
    def xlsx_blob_(self, request):
        return instance_mock(request, bytes)

    @pytest.fixture
    def xlsx_file_(self, request, xlsx_blob_):
        xlsx_file_ = instance_mock(request, BytesIO)
        xlsx_file_.getvalue.return_value = xlsx_blob_
        return xlsx_file_
