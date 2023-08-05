#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyccuracy.page import PageRegistry, Page
from pyccuracy.actions import ActionBase
from pyccuracy.languages import LanguageItem

def resolve_element_key(context, element_type, element_name, resolve_function):
    element_category = context.language.get(element_type.encode("utf-8") + "_category")
    return resolve_function(context, element_category, element_name)

class SelectOptionByValueAction(ActionBase):
    regex = LanguageItem("select_option_by_value_regex")

    def execute(self, context, select_name, option_value):
        select_key = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select_key, error_message)
        
        result = context.browser_driver.select_option_by_value(select_key, option_value)
        
        if not result:
            error_message = context.language.format("select_option_by_value_failure", select_name, option_value)
            raise self.failed(error_message)

class SelectHasSelectedValueAction(ActionBase):
    regex = LanguageItem("select_has_selected_value_regex")

    def execute(self, context, select_name, option_value):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)
        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select, error_message)
        
        selected_value = context.browser_driver.get_selected_value(select)

        if (unicode(selected_value) != unicode(option_value)):
            error_message = context.language.format("select_has_selected_value_failure", select_name, option_value, selected_value)
            raise self.failed(error_message)

class SelectOptionByIndexAction(ActionBase):
    regex = LanguageItem("select_option_by_index_regex")

    def execute(self, context, select_name, index):
        index = int(index)
        select_key = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select_key, error_message)
        
        result = context.browser_driver.select_option_by_index(select_key, index)
        
        if not result:
            error_message = context.language.format("select_option_by_index_failure", select_name, index)
            raise self.failed(error_message)

class SelectHasSelectedIndexAction(ActionBase):
    regex = LanguageItem("select_has_selected_index_regex")

    def execute(self, context, select_name, index):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)
        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select, error_message)
        
        selected_index = context.browser_driver.get_selected_index(select)

        if (int(selected_index) != int(index)):
            error_message = context.language.format("select_has_selected_index_failure", select_name, index, selected_index)
            raise self.failed(error_message)

class SelectOptionByTextAction(ActionBase):
    regex = LanguageItem("select_option_by_text_regex")

    def execute(self, context, select_name, text):
        select_key = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select_key, error_message)
        
        result = context.browser_driver.select_option_by_text(select_key, text)
        
        if not result:
            error_message = context.language.format("select_option_by_text_failure", select_name, text)
            raise self.failed(error_message)

class SelectHasSelectedTextAction(ActionBase):
    regex = LanguageItem("select_has_selected_text_regex")

    def execute(self, context, select_name, text):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)
        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select, error_message)

        selected_text = context.browser_driver.get_selected_text(select)

        if (selected_text != text):
            error_message = context.language.format("select_has_selected_text_failure", select_name, text, selected_text)
            raise self.failed(error_message)

class SelectDoesNotHaveSelectedIndexAction(ActionBase):
    regex = LanguageItem("select_does_not_have_selected_index_regex")

    def execute(self, context, select_name, index):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select, error_message)

        selected_index = context.browser_driver.get_selected_index(select)

        if (selected_index == index):
            error_message = context.language.format("select_does_not_have_selected_index_failure", select_name, index, selected_index)
            raise self.failed(error_message)

class SelectDoesNotHaveSelectedValueAction(ActionBase):
    regex = LanguageItem("select_does_not_have_selected_value_regex")

    def execute(self, context, select_name, value):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select, error_message)

        selected_value = context.browser_driver.get_selected_value(select)

        if (selected_value == value):
            error_message = context.language.format("select_does_not_have_selected_value_failure", select_name, value, selected_value)
            raise self.failed(error_message)

class SelectDoesNotHaveSelectedTextAction(ActionBase):
    regex = LanguageItem("select_does_not_have_selected_text_regex")

    def execute(self, context, select_name, text):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)
        self.assert_element_is_visible(context, select, error_message)

        selected_text = context.browser_driver.get_selected_text(select)

        if (selected_text == text):
            error_message = context.language.format("select_does_not_have_selected_text_failure", select_name, text, selected_text)
            raise self.failed(error_message)

class SelectContainsOptionWithTextAction(ActionBase):
    regex = LanguageItem("select_contains_option_with_text_regex")

    def execute(self, context, select_name, text):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)

        self.assert_element_is_visible(context, select, error_message)

        options = context.browser_driver.get_select_options(select)

        found = text in options
        
        if not found:
            error_message = context.language.format("select_contains_option_with_text_failure", select_name, text)
            raise self.failed(error_message)

class SelectDoesNotContainOptionWithTextAction(ActionBase):
    regex = LanguageItem("select_does_not_contain_option_with_text_regex")

    def execute(self, context, select_name, text):
        select = resolve_element_key(context, Page.Select, select_name, self.resolve_element_key)

        error_message = context.language.format("element_is_visible_failure", Page.Select, select_name)

        self.assert_element_is_visible(context, select, error_message)

        options = context.browser_driver.get_select_options(select)

        found = text in options
        
        if found:
            error_message = context.language.format("select_does_not_contain_option_with_text_failure", select_name, text)
            raise self.failed(error_message)

