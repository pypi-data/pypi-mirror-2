#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010 Tobi Vollebregt

from contextlib import closing
from ConfigParser import RawConfigParser as ConfigParser
from progressbar import ProgressBar
import rapid
import getopt, gzip, os, sys
import re
import logging


log = logging.getLogger('root')


class TextUserInteraction:
	def __init__(self, force=False):
		self.force = force

	def confirm(self, text):
		""" Ask the user for confirmation."""
		return self.force or raw_input(text + ' [y/N]: ').startswith('y')

	def _to_i_bounds_check(self, text, lower, upper):
		i = int(text)
		if i < lower or i > upper:
			# raise IndexError with standard message
			arr = [] ; arr[i]
		return i

	def choose_many(self, header, options, question):
		""" Let the user choose multiple options from a list."""
		print header
		for i in range(len(options)):
			print '%2i.  %s' % (i + 1, options[i])
		which = raw_input(question + ' [enter number(s) or "all"]: ')
		if which.lower().strip() == 'all':
			return options
		which = re.split(r'[\s,]+', which)
		try:
			n = len(options)
			which = [self._to_i_bounds_check(x, 1, n) - 1 for x in which]
		except (ValueError, IndexError) as e:
			print type(e).__name__ + ':', str(e)
			return []
		return [options[x] for x in which]

	def _select_core(self, needle, haystack):
		""" Override/patch this to implement other search strategy.
		This variant implements a simple case-insensitive substring search."""
		n = needle.lower()
		return filter(lambda s: n in str(s).lower(), haystack)

	def select(self, noun, needle, haystack):
		""" Select items from a list based on needle, and take appropriate
		action based on the number of results this returns."""
		selected = self._select_core(needle, haystack)

		if len(selected) == 0:
			print 'No %ss matching "%s" found.' % (noun, needle)
			return selected

		if len(selected) >= 100:
			print '100 or more %ss matching "%s" found, please narrow your search.' % (noun, needle)
			return []

		if len(selected) > 1:
			return self.choose_many('Multiple %ss matching "%s" found:' % (noun, needle), selected, 'Which %s do you mean?' % noun)

		return selected

	def output_header(self, text):
		""" Output the header of a list/table."""
		print text

	def output_detail(self, text):
		""" Output a detail row of a list/table.
		TODO: Interface should be improved."""
		print text

	def important_warning(self, *lines):
		""" Display an important warning to the user."""
		print
		print '#' * 79
		for line in lines:
			print '# %-75s #' % line.center(75)
		print '#' * 79
		print


def init(data_dir, _ui):
	"""  Create rapid module."""
	global spring_dir, pool_dir, rapid, ui
	ui = _ui

	log.info('Using data directory: %s', data_dir)
	rapid.set_spring_dir(data_dir)

	# Global constants/rapid instance.
	spring_dir = rapid.spring_dir
	pool_dir = rapid.pool_dir
	rapid = rapid.Rapid()


def pin_single(tag):
	""" Pin a tag. This means any package having this tag will automatically be
	    installed and upgraded."""
	if not tag in rapid.pinned_tags:
		log.info('Pinning: %s', tag)
		rapid.pinned_tags.add(tag)
	else:
		log.info('Already pinned: %s', tag)


def pin(searchterm):
	""" Pin all tags matching searchterm and install the corresponding packages."""
	for t in ui.select('tag', searchterm, rapid.tags):
		pin_single(t)
		install_single(rapid.packages[t])


def unpin_single(tag):
	""" Unpin a tag. This means packages having this tag will not be
	    automatically upgraded anymore. Does not uninstall anything."""
	if tag in rapid.pinned_tags:
		log.info('Unpinning: %s', tag)
		rapid.pinned_tags.remove(tag)
	else:
		log.info('Not pinned: %s', tag)


def unpin(searchterm):
	""" Unpin all tags matching searchterm."""
	for t in ui.select('pinned tag', searchterm, rapid.pinned_tags):
		unpin_single(t)


def install_single(p, dep = False):
	""" Install a single package and its dependencies."""
	if p:
		for d in p.dependencies:
			install_single(d, True)
		if not p.installed:
			log.info('Installing%s: %s', ' dependency' if dep else '', p.name)
			p.install(ProgressBar())
		elif not dep:
			log.info('Already installed: %s', p.name)


def install(searchterm):
	""" Install all packages matching searchterm."""
	for name in ui.select('name', searchterm, [p.name for p in rapid.packages]):
		install_single(rapid.packages[name])


def uninstall_single(p):
	""" Uninstall and unpin a single package. Does not uninstall dependencies."""
	if p:
		if not p.can_be_uninstalled:
			log.error('Can not uninstall because of dependencies: %s', p.name)
			return
		for t in p.tags:
			unpin_single(t)
		log.info('Uninstalling: %s', p.name)
		p.uninstall()


def uninstall_single_plus_revdeps(p, dep = False):
	""" Uninstall and unpin a package and all packages that depend on it."""
	if p:
		for d in p.reverse_dependencies:
			uninstall_single_plus_revdeps(d, True)
		for t in p.tags:
			unpin_single(t)
		if p.installed:
			log.info('Uninstalling%s: %s', ' dependency' if dep else '', p.name)
			p.uninstall()
		elif not dep:
			log.info('Already uninstalled: %s', p.name)


def uninstall(searchterm):
	""" Uninstall all packages matching searchterm."""
	for name in ui.select('name', searchterm, [p.name for p in rapid.packages if p.installed]):
		uninstall_single(rapid.packages[name])


def list_packages(searchterm, available):
	""" List all packages whose name matches searchterm."""
	ui.output_header('Installed packages:')
	for p in sorted(ui._select_core(searchterm, rapid.packages), key = str):
		if p.installed:
			ui.output_detail('  %-40s (%s)' % (p.name, ', '.join(p.tags)))
	if available:
		ui.output_header('Available packages:')
		for p in sorted(ui._select_core(searchterm, rapid.packages), key = str):
			if not p.installed:
				ui.output_detail('  %-40s (%s)' % (p.name, ', '.join(p.tags)))


def list_tags(searchterm, available):
	""" List all tags which match searchterm."""
	ui.output_header('Pinned tags:')
	for tag in sorted(ui._select_core(searchterm, rapid.pinned_tags)):
		p = rapid.packages[tag]
		if p:
			ui.output_detail('  %-40s (%s)' % (tag, p.name))
		else:
			ui.output_detail('  %-40s [dangling tag]' % tag)
	if available:
		ui.output_header('Available tags:')
		for tag in sorted(ui._select_core(searchterm, rapid.tags)):
			if tag not in rapid.pinned_tags:
				p = rapid.packages[tag]
				ui.output_detail('  %-40s (%s)' % (tag, p.name))


def upgrade():
	""" Upgrade pinned tags."""
	for tag in rapid.pinned_tags:
		install_single(rapid.packages[tag])


def clean_upgrade():
	""" Upgrade pinned tags and uninstall unpinned packages."""
	upgrade()
	uninstall_unpinned()


def uninstall_unpinned():
	""" Simple mark and sweep garbage collector. The root set consists of the
	    pinned tags. This does not touch pool files."""
	# Build set marked_packages that should be kept.
	marked_packages = set()
	new_packages = set(rapid.packages[t] for t in rapid.pinned_tags if t in rapid.tags)
	while new_packages:
		marked_packages.update(new_packages)
		new_packages = sum([list(p.dependencies) for p in new_packages], [])

	# Build set of packages that will be removed.
	garbage = set(set(p for p in rapid.packages if p.installed) - marked_packages)

	# Anything to do?
	if not garbage:
		log.info('Nothing to do.')
		return

	# Confirmation?
	if not ui.confirm('Uninstall %s?' % ', '.join(p.name for p in garbage)):
		return

	# Uninstall all garbage.
	for p in garbage:
		if p.installed:
			uninstall_single_plus_revdeps(p)


def collect_pool():
	""" Simple mark and sweep garbage collector. The root set consists of the
	    installed packages. This touches only pool files."""
	# Build set marked_files that should be kept.
	installed_packages = [p for p in rapid.packages if p.installed]
	marked_files = reduce(lambda x, y: x + y.files, installed_packages, [])
	marked_files = set(f.pool_path for f in marked_files)

	def gc(really_remove):
		# Remove all files not in marked_files.
		count = 0
		size = 0
		for i in range(0, 256):
			d = os.path.join(pool_dir, '%02x' % i)
			for f in os.listdir(d):
				f = os.path.join(d, f)
				if not f in marked_files:
					count += 1
					size += os.path.getsize(f)
					if really_remove: os.unlink(f)
		return (count, size)

	count, size = gc(False)

	log.info('%.2f megabytes / %d files can be collected from the pool.', size / (1024.*1024.), count)
	if count == 0:
		return

	# Confirmation?
	ui.important_warning(
		'Collecting pool files will delete the data from disk permantly.',
		'You will have to download the data again in case you need it.')

	if not ui.confirm('Delete %d pool files?' % count):
		return

	count, size = gc(True)
	log.info('%.2f megabytes / %d files deleted from the pool.', size / (1024.*1024.), count)


def make_sdd(package, path):
	""" Extract all files for a single package from the pool and put them in
	    a newly created .sdd package."""
	if package not in rapid.packages:
		log.error('Package %s not known', package)
		return
	package = rapid.packages[package]
	if not os.path.exists(os.path.dirname(path)):
		path = os.path.join(spring_dir, 'mods', path)
	if os.path.exists(path):
		log.error('%s already exists', path)
		return

	missing_files = package.missing_files
	if missing_files:
		log.info('Downloading %d missing files for: %s', len(missing_files), package.name)
		package.download_files(missing_files, ProgressBar())

	files = package.files
	log.info('Extracting %d files into: %s', len(files), path)
	progress = ProgressBar(maxValue = len(files))
	for f in files:
		target_name = os.path.join(path, f.name)
		if not os.path.exists(os.path.dirname(target_name)):
			os.makedirs(os.path.dirname(target_name))
		with closing(gzip.open(f.pool_path, 'rb')) as source:
			with closing(open(target_name, 'wb')) as target:
				target.write(source.read())
		progress(1)
